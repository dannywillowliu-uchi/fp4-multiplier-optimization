# FP4 Multiplier Gate Optimization

Minimizing the gate count of a Boolean circuit implementing FP4 (MxFP4) floating-point multiplication.

**Current best: 54 gates** (20 AND + 8 OR + 26 XOR + 0 NOT), down from 205 gates (73.7% reduction).

## Problem Statement

Given two 4-bit FP4 encoded inputs (8 input bits total), compute `a * b * 4` as a 9-bit two's complement integer using the minimum number of {AND, OR, XOR, NOT} gates.

### FP4 Encoding (MxFP4)

| Code | Value | Code | Value |
|------|-------|------|-------|
| 0000 |  0.0  | 1000 |  0.0  |
| 0001 |  0.5  | 1001 | -0.5  |
| 0010 |  1.0  | 1010 | -1.0  |
| 0011 |  1.5  | 1011 | -1.5  |
| 0100 |  2.0  | 1100 | -2.0  |
| 0101 |  3.0  | 1101 | -3.0  |
| 0110 |  4.0  | 1110 | -4.0  |
| 0111 |  6.0  | 1111 | -6.0  |

- Bit 3 is the sign bit
- Bits [2:0] encode the magnitude: {0, 0.5, 1, 1.5, 2, 3, 4, 6}
- Output range: [-144, +144], encoded as 9-bit two's complement
- 256-entry truth table (16 x 16 inputs), 37 unique output values, 60 zero entries

### Gate Model

- Available gates: AND, OR, XOR, NOT (each costs 1 gate)
- 2-input gates only (except NOT which is 1-input)
- Fan-out is free (any gate output can feed multiple inputs)
- No latches/memory -- purely combinational

## Optimization Timeline

```
205 -> 87 -> 83 -> 77 -> 73 -> 71 -> 69 -> 67 -> 66 -> 65 -> 64
 -> 63 -> 62 -> 61 -> 60 -> 59 -> 58 -> 57 -> 56 -> 54
```

### Full Cascade History

| Gates | Method | Key Details |
|------:|--------|------------|
| 205 | Baseline | Naive sum-of-products from truth table |
| 87 | CGP | Cartesian Genetic Programming initial optimization |
| 83 | CGP | Further CGP evolution |
| 77 | SA | Simulated annealing first major breakthrough |
| 73 | SA | Continued SA optimization |
| 71 | SA | SA with 50M step budget |
| 69 | SAT Peephole | Window-4 SAT-based peephole found 2 replacements |
| 67 | SA | SA from 69, found 67 |
| 66 | SA | SA from 67, two different 66-gate topologies found |
| 65 | SA | Enhanced SA with larger mutations |
| 64 | SAT Peephole | W9 random peephole on ga-fp6227 (structurally diverse 65-gate circuit) |
| 63 | SAT Peephole | W7 peephole on 64-gate circuit |
| 62 | SA | SA from 63 (3 workers found it independently) |
| 61 | SA | SA-0 from 62, step 46M/50M budget |
| 60 | SA | SA-3 from 61, step 74M/100M budget |
| 59 | SA | SA-200 from 60, step 184M/300M budget |
| 58 | SA | SA-307 from 59, step 267M/300M budget (t=40, hot exploration) |
| 57 | SAT Peephole | W7 peephole on 58 (window [34,38,40,43,53,54,56], DC ratio 0.836) |
| 56 | SA | SA-606 from 57, step 263M/500M budget (t=40, cool=0.9999940) |
| **54** | **SA** | **SA-703 from 56, step 16.7M/500M budget (t=30). Also SA-700 found 54 independently at step 269M.** |

### SA Budget Scaling Pattern

| Transition | Steps to Find | Budget | Workers | Temperature |
|-----------|--------------|--------|---------|-------------|
| 62 -> 61 | 46M | 50M | 8 | default |
| 61 -> 60 | 74M | 100M | 8 | default |
| 60 -> 59 | 184M | 300M | 8 | default |
| 59 -> 58 | 267M | 300M | 8 | t=40 (hot) |
| 58 -> 57 | peephole | - | - | - |
| 57 -> 56 | 263M | 500M | 8 | t=40, cool=0.9999940 |
| 56 -> 54 | 16.7M | 500M | 8 | t=30 (2-gate jump!) |

The 56->54 jump was anomalous: SA found a 2-gate improvement in only 16.7M steps, while most single-gate improvements required 100M+ steps. Multiple workers found 54 and 55-gate circuits, suggesting the landscape opened up dramatically at 56 gates.

## Methods

### Simulated Annealing (SA)

The primary optimization engine. Uses a DAG-based circuit representation with:
- **Mutations**: Gate type change, input rewiring, gate insertion/deletion, subcircuit rewiring
- **Evaluation**: Full 256-row truth table verification
- **Diverse seeding**: Running from multiple topologically different circuits
- **Reheating**: Periodic temperature increases to escape local optima
- Parallel workers (typically 8) with varied temperature/cooling schedules

### SAT-Based Peephole Optimization

Selects a window of W gates and asks a SAT solver: "can these W gates be replaced by W-1 gates that produce the same outputs?" Key details:
- Uses PySAT (Glucose4 solver) with conflict budget for timeouts
- **Don't-care ratio (DC)**: Windows where fewer input patterns are reachable have more freedom for the SAT solver. High DC ratio correlates with SAT success.
- Exhaustive enumeration for window sizes 4-7; DC-scored sampling for sizes 8-9
- Cycle detection and topological sort for circuit reconstruction
- Proven effective at sizes where SA struggles (local refinement)

### Cartesian Genetic Programming (CGP)

Used in early stages (205->87->83). Evolves circuits on a grid-based representation. Less effective than SA for fine-grained optimization but good for initial structure discovery.

### Genetic Algorithm with Diversity

A population-based search maintaining structurally diverse circuits. The circuit `ga-fp6227` (a 65-gate circuit from this method) proved critical: its different topology led to the 64-gate breakthrough via peephole, which cascaded all the way down to 54.

## Current Best Circuit (54 Gates)

```python
def fp4_multiply(a3, a2, a1, a0, b3, b2, b1, b0):
    # 54 gates: 20 AND + 8 OR + 26 XOR + 0 NOT
    g0 = b2 | b1
    g1 = b2 & a2
    g2 = b2 ^ a2
    g3 = b0 ^ g0
    g4 = a1 & b1
    g5 = a1 | a2
    g6 = a1 | b1
    g7 = g5 ^ a0
    g8 = g3 | g7
    g9 = g7 & g3
    g10 = a3 ^ b3
    g11 = g6 ^ g4
    g12 = g8 ^ g4
    g13 = g3 | b0
    g14 = g5 | g7
    g15 = g9 & g11
    g16 = g14 & g13
    g17 = g1 & g6
    g18 = g16 ^ g15
    g19 = g2 ^ g12
    g20 = g9 ^ g18
    g21 = g12 ^ g1
    g22 = g19 & g18
    g23 = g11 ^ g19
    g24 = g12 & g4
    g25 = g21 & g22
    g26 = g23 & g20
    g27 = g21 & g17
    g28 = g10 & g16
    g29 = g26 ^ g20
    g30 = g10 & g9
    g31 = g24 & g17
    g32 = g1 | g24
    g33 = g28 ^ g31
    g34 = g32 & g29
    g35 = g28 ^ g25
    g36 = g26 ^ g33
    g37 = g27 ^ g28
    g38 = g28 ^ g34
    g39 = g10 & g35
    g40 = g38 ^ g29
    g41 = g37 ^ g18
    g42 = g39 & g40
    g43 = g22 ^ g41
    g44 = g42 & g43
    g45 = g36 & g44
    g46 = g22 ^ g35
    g47 = g45 & g46
    g48 = g37 | g30
    g49 = g38 ^ g47
    g50 = g36 ^ g44
    g51 = g43 ^ g42
    g52 = g45 ^ g46
    g53 = g39 ^ g40
    return [g28, g33, g48, g49, g52, g50, g51, g53, g25]
```

Verified correct on all 256 input combinations.

## Circuit Analysis

### Structural Properties

| Property | Value |
|----------|-------|
| Total gates | 54 |
| Gate mix | 20 AND + 8 OR + 26 XOR + 0 NOT |
| Circuit depth | 16 |
| NOT gates | 0 (all eliminated) |
| Gate sharing | 81.1% of gate-uses shared across outputs |
| Bottleneck gate | g28 (AND) with fanout 5, feeds all 9 outputs |

### Decomposition

The circuit naturally splits into two stages:

- **Stage 1 (Magnitude core)**: 31 gates, independent of sign bits (a3, b3). Computes the unsigned magnitude product from the 6 magnitude inputs.
- **Stage 2 (Sign handling)**: 23 gates, depends on a3/b3. Performs conditional two's complement negation, zero masking, and sign extension.

The sign handling is 3-5 gates more efficient than the textbook approach (conditional invert + ripple carry ≈ 26-28 gates).

### Algebraic Properties

- Output o0 (LSB) depends on only 4 inputs: {a0, a1, b0, b1}
- All other outputs depend on all 8 inputs
- 139 unique nonlinear ANF terms across all 9 outputs (max algebraic degree 7)
- Bilinear GF(2) rank: 3 (the degree-2 structure is simple despite high overall complexity)

### FP4-Specific Structure

Each FP4 magnitude factors as m * 2^k where m in {1, 3} and k in {-1, 0, 1, 2}:
- m=3 when `b0 AND (b1 OR b2)`
- The product decomposes as: (m_a * m_b) * 2^(k_a + k_b)
- But the encoding irregularity (code 001 has m=1, not m=3) prevents a perfectly clean gate-level decomposition

## Lower Bounds

| Method | Bound | Notes |
|--------|-------|-------|
| Per-bit independent SAT | 67 gates | Sum of SAT-proven optimal per output bit. We beat this by 13 gates, proving inter-output sharing saves at least 13 gates. |
| Multi-output SAT exact | ~14 gates | True multi-output bound is too loose (SAT infeasible at useful sizes) |
| Bilinear GF(2) rank | 3 AND gates | Only bounds the degree-2 terms, very loose |
| Estimated true optimum | 45-54 gates | Based on algebraic complexity analysis and circuit structure efficiency |

**Gap analysis**: The true optimum lies in [14, 54]. Our analysis suggests it's likely in [45, 54], meaning the current circuit is within 0-9 gates of optimal.

## Key Lessons Learned

1. **SA + peephole alternation** is the most effective strategy. SA breaks through plateaus; peephole finds local improvements that SA misses.

2. **Structural diversity is essential**. The circuit ga-fp6227 (from genetic search) had a fundamentally different topology. Starting SA/peephole from it led to the 64-gate breakthrough, cascading all the way to 54.

3. **Increasing SA budgets** are needed as gates decrease. Each gate reduction requires roughly 2-3x more SA steps, with hot exploration (high initial temperature) becoming increasingly important.

4. **Don't-care ratio** is the key metric for SAT peephole. Windows with high DC ratio (fewer reachable input patterns) give the SAT solver more freedom, dramatically increasing success probability.

5. **The landscape can open up unexpectedly**. The 56->54 jump (2 gates in 16.7M steps) was far faster than the typical single-gate improvements (~100M+ steps). Multiple workers finding 54/55 suggests the 56-gate circuit was on a ridge between basins.

6. **Zero NOT gates** is achievable. Both 54-gate topologies eliminated all NOT gates, suggesting the function's algebraic structure doesn't inherently require complementation.

## Repository Structure

```
README.md                   # This report
circuits/
  optimized_54_gates.py     # Current best (54 gates)
  optimized_56_gates.py     # Previous best (56 gates)
  optimized_57_gates.py     # Previous (57 gates)
  optimized_58_gates.py     # Previous (58 gates)
  optimized_205_gates.py    # Baseline circuit
  circuit_54g_alt.py        # Alternative 54-gate topology (SA-700)
fp4_multiplier.py           # Truth table generation and verification
```

## What's Next

Potential approaches to beat 54 gates:

1. **Algebraic Seed + SA**: Construct circuits from the FP4 algebraic structure (sign-magnitude decomposition), use as SA seeds to explore different basins of attraction.

2. **ABC Logic Synthesis**: Export to AIG format, run ABC's algebraic rewriting, tech-map back to {AND, OR, XOR}.

3. **SAT on sub-functions**: Prove optimal sizes for magnitude output groups, identify sharing limits.

4. **BDD-based synthesis**: Different structural decomposition methodology.
