# How I Solved This: LLM-Assisted Circuit Optimization

## Approach

I used LLM agents (Claude Code) as a reasoning and implementation partner to iteratively optimize an FP4 multiplier circuit from 205 gates down to 54. The agent handled code generation, algorithm implementation, and result analysis while I directed strategy and decided when to pivot approaches.

The core loop was: **run -> analyze results -> diagnose the bottleneck -> design the next approach -> repeat.**

---

## Phase 1: Understanding the Problem (Feb 4)

**20 files created in one evening session.**

The first task was making sense of the problem. The agent parsed the PDF spec, understood the FP4 encoding (a non-uniform 4-bit floating point format mapping to values like 0, 0.5, 1, 1.5, 2, 3, 4, 6 and their negatives), and built the core infrastructure:

- `fp4_multiplier.py` -- truth table generator and `verify_circuit()` function that checks all 256 input combinations
- Multiple circuit construction attempts (`solution.py`, `complete_circuit.py`, `manual_circuit.py`, `working_circuit.py`) -- the agent kept building circuits, testing them against the truth table, finding failures, and iterating

The agent also explored the problem space: what symmetries exist in the truth table, whether input remapping could help, whether SAT solvers could directly synthesize small circuits.

**Key outcome**: No optimized circuit yet, but solid infrastructure for verification and a growing understanding of the problem's structure.

---

## Phase 2: Structural Decomposition (Feb 5)

**22 files. First working optimized circuits: 205 -> 90 -> 87 gates.**

I had the agent break the problem down mathematically. FP4 multiplication decomposes naturally into sub-problems:

1. **Sign computation**: Output is negative iff exactly one input is negative = `a3 XOR b3` (1 gate)
2. **Zero detection**: Both 0000 and 1000 encode zero; if either operand is zero, output is all zeros
3. **Magnitude multiplication**: The non-sign bits encode magnitudes that can be split into exponent and mantissa parts
4. **Conditional negation**: If the result is negative, negate the magnitude via two's complement (carry chain)

Each sub-circuit was designed by the agent using basic logic design. The naive first pass was 205 gates; optimizing redundant patterns brought it to 87.

The agent also explored alternative tools: ABC (Berkeley logic synthesis tool), BLIF format export, SAT-based exact synthesis. SAT exact synthesis showed the problem is too large for exact methods on the full circuit. Per-bit lower bound analysis proved any circuit needs at least 67 gates if each output is computed independently.

**Key learning**: Hand-design hits a wall. Exact methods are intractable on the full problem. Need automated search.

---

## Phase 3: Evolutionary Search (Feb 7)

**11 files. CGP: 87 -> 86 -> 85 -> 84 -> 83 gates.**

The agent implemented Cartesian Genetic Programming (CGP), which represents the circuit as a grid of nodes and evolves it by mutating gate types and connections. Seeded from the 87-gate structural circuit, CGP found improvements quickly -- reaching 83 gates in about 60 seconds.

CGP works through neutral drift: most mutations hit "inactive" nodes (not connected to outputs), but occasionally a reconnection routes through a shorter path. This finds optimizations that are hard to spot manually.

**Key learning**: Evolutionary search beats hand-design, but CGP plateaued at 83. Its one-mutation-at-a-time strategy can't make coordinated multi-gate changes.

---

## Phase 4: SA + Peephole Alternation (Feb 9, morning)

**This was the key methodological breakthrough.**

The agent built `sa_dag_search.py` -- simulated annealing operating directly on the circuit DAG (unlike CGP's fixed grid, SA could add/remove gates). SA uses a temperature schedule where it starts accepting bad moves freely, then gradually becomes greedy. Seven mutation operators: rewire inputs (35%), change gate type (15%), remove gate (15%), insert gate (10%), swap gates (5%), change output wiring (5%), multi-rewire (15%).

SA rapidly optimized: 83 -> 82 -> 81 -> ... -> 77. Then it got stuck.

**Diagnosing the plateau**: The agent analyzed SA's behavior -- acceptance rate was still ~11%, temperature was reasonable, but no improving moves existed in the local neighborhood. The mutations only change 1-3 elements at a time; escaping required a coordinated change to 4+ gates simultaneously.

**The complementary approach**: The agent proposed SAT-based peephole optimization. This extracts a small window of k gates, builds a truth table for just that window (crucially exploiting "don't-care" inputs that never actually occur), and asks a SAT solver: "can this be done with k-1 gates?" The SAT solver explores the *entire* space of possible replacements exhaustively.

Peephole broke the plateau: windows that SA would need impossibly coordinated moves to find were trivially found by SAT.

The alternation pattern emerged:
```
SA: 83 -> 77 (stuck)
Peephole: 83 -> 78 (different path)
SA re-seeded: 77 -> 71 (stuck)
Peephole: 71 -> 69 (two window replacements)
SA: 69 -> 67 (stuck)
Peephole: 67 -> 66 (one window replacement)
SA independently also found 66
```

Each time peephole removed a gate, the circuit topology changed just enough to give SA a new landscape. Neither method alone could have reached 66.

---

## Phase 5: Population Diversity (Feb 9, afternoon)

**81 files created this day total. GA + enhanced SA: 66 -> 65 -> 64 -> 63.**

Both SA and peephole exhausted at 66. The agent analyzed the logs: 79 SA trials stuck at 66, all peephole windows size 4-7 checked with zero improvements. Diagnosis: the search had converged to a single basin in the optimization landscape.

The agent proposed two solutions:

1. **Enhanced SA** (`sa_enhanced.py`): Richer mutations including subcircuit transplant (replace a random 3-5 gate sub-DAG with a fresh random one) and macro-mutations (remove 2-3 gates, add 1-2). Found 65 gates.

2. **Genetic algorithm** (`ga_search.py`): Maintains a population of 50 circuits with crossover between them. Even if all circuits are 65-66 gates, they have different internal structures. Different structures expose different peephole windows and different SA trajectories.

The GA produced many structurally diverse 65-66 gate circuits. Peephole on GA circuit fp6227 found a 9->8 gate window (65 -> 64). Peephole on that found 64 -> 63.

---

## Phase 6: Diverse Seeds Push to 54 (Feb 9-10)

**63 -> 62 -> 61 -> 60 -> 59 -> 58 -> 57 -> 56 -> 54.**

`sa_diverse_seeds.py` ran many SA instances from different starting circuits. The alternation continued:

| Gates | Method | Source |
|-------|--------|--------|
| 62 | SA-diverse run 3 | from 63-gate seed |
| 61 | SA-diverse run 0 | from 62-gate seed |
| 60 | SA-diverse run 3 | from 61-gate seed |
| 59 | SA-diverse run 200 | from 60-gate seed |
| 58 | SA-diverse run 307 | from 59-gate seed |
| 57 | SAT peephole | window [34,38,40,43,53,54,56] 7->6 on 58-gate |
| 56 | SA-diverse run 606 | from 57-gate seed |
| **54** | **SA-diverse run 703** | **from 56-gate seed, step 16.7M** |

The 54-gate circuit was also found independently by run 700 at step 269M with a different topology, suggesting 54 is a robust attractor in the search landscape.

---

## Phase 7: Attempting to Break 54 (Feb 10-19)

Multiple attempts to go below 54, all unsuccessful:

- `sa_from_54.py`, `sa_from_54_v2.py`, `sa_from_54_v3.py` -- SA stuck at 54 across many trials
- `peephole_54.py` -- all windows size 4-7 checked, zero improvements (locally optimal)
- `peephole_w8_54.py`, `peephole_w9_54.py` -- larger windows up to size 9, still no improvements
- `sa_diverse_basins.py` -- tried completely different starting structures
- Analysis (`output_cone_analysis.py`, `boyar_peralta.py`) deepened understanding of why 54 might be near-optimal

---

## What Made This Work

### The agent as a reasoning partner

The agent wasn't just generating code. At each plateau, it:
1. **Analyzed logs and results** to identify *why* the current method was stuck
2. **Diagnosed the structural cause** (e.g., "SA mutations are too local" or "search has converged to a single basin")
3. **Proposed the specific complementary approach** that addresses that weakness
4. **Implemented it**, including all the complexity of SAT encoding, GA crossover operators, etc.

### The meta-strategy

The breakthrough wasn't any single algorithm. It was the pattern of **alternating between complementary methods**:
- SA for global restructuring, peephole for exact local rewriting
- Population diversity (GA) when single-trajectory search converges
- Re-seeding SA from each improvement to explore new neighborhoods

This is essentially iterated local search with heterogeneous neighborhood operators, but the specific combination applied to circuit minimization -- and the reasoning about *when and why* to switch methods -- was driven by the LLM agent's analysis at each step.

### Verification discipline

Every candidate circuit was verified against all 256 input combinations via `verify_circuit()`. The verification function was built on day 1 and never changed. This caught many incorrect circuits during SA and GA exploration (correctness is part of the fitness function, not an afterthought).

---

## By the Numbers

- **Total Python files created**: ~200+
- **Days active**: ~12 (Feb 4-16)
- **Gate reduction**: 205 -> 54 (73.7%)
- **Methods used**: Hand design, CGP, SA, SAT peephole, GA, enhanced SA, diverse seeding
- **SA plateaus broken by peephole**: 5 (at 83, 71, 67, 65, 58)
- **Independent 54-gate circuits found**: 2 (different topologies)
- **Verification**: 256/256 correct on all submitted circuits
