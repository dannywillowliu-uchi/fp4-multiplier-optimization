# FP4 Multiplier Optimization

Minimum-gate Boolean circuit for multiplying two MxFP4 numbers.
See [`take-home-spec.pdf`](take-home-spec.pdf) for the original problem statement.

## The Problem

Design a circuit using the fewest 2-input AND, OR, XOR and 1-input NOT gates that computes `(a * b * 4)` for two 4-bit MxFP4 inputs, producing a 9-bit two's complement output.

**MxFP4** encodes 16 values: `{0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6}` in 4 bits (sign-magnitude, with two representations of zero). The circuit must be correct for all 256 input combinations. Input remapping (same bijection on both inputs) is free; output remapping is not allowed.

### Why This Is Hard

This is the **Minimum Circuit Size Problem (MCSP)**: given a truth table, find the smallest Boolean circuit that computes it. MCSP is known to be NP-hard, and no polynomial-time algorithm exists.

- **Search space**: a circuit with *n* gates over 8 inputs has roughly `(4 × n²)^n` possible topologies -- for n=50 that's ~10^170.
- **Exact synthesis** (SAT/SMT) can prove optimality for small circuits, but becomes intractable beyond ~15-20 gates. Our 9-output, 8-input function is far beyond this horizon.
- **Standard integer multipliers**: a 4×4 unsigned integer multiplier typically needs ~100 gates. FP4's irregular encoding (non-uniform spacing, two zeros, sign-magnitude) makes classical multiplier architectures a poor fit.
- **Lower bounds**: SAT-proven per-bit independent synthesis requires at least **67 gates** (sum over all 9 outputs synthesized separately). The true multi-output optimum is unknown -- the gap between 14 (trivial partition bound) and 54 (our best) is open.

### What "Good" Looks Like

| Range | Assessment |
|-------|------------|
| >100 gates | Naive / textbook approach |
| 70-100 | Reasonable logic synthesis (Espresso, ABC) |
| 50-70 | Strong optimization, exploits FP4 structure |
| 40-50 | Likely near-optimal; requires deep inter-output sharing |
| <40 | Would require a breakthrough or proof of impossibility |

## Result: 54 Gates

**20 AND + 8 OR + 26 XOR + 0 NOT = 54 gates** -- verified 256/256 correct.

Found by simulated annealing (run 703, step 16.7M, T=30) from a 56-gate seed.
Independently confirmed by run 700 (step 269M, different topology).

This is **13 gates below the per-bit lower bound** of 67, proving that inter-output gate sharing saves at least 13 gates in this circuit.

See [`optimized_54_gates.py`](optimized_54_gates.py) for the implementation.

### Optimization Trace
```
205 -> 87 -> 83 -> 77 -> 73 -> 71 -> 69 -> 67 -> 66 -> 65 -> 64 -> 63 -> 62 -> 61 -> 60 -> 59 -> 58 -> 57 -> 56 -> 54
```

Techniques used in cascade:
- **Structural decomposition** (205 -> 87): hand-built sign-magnitude architecture
- **CGP** (87 -> 83): Cartesian Genetic Programming with neutral drift
- **Simulated annealing on circuit DAG** (83 -> 57): 7 mutation operators, 256-bit vectorized evaluation
- **SAT peephole optimization**: exact k-gate window replacement via PySAT (CaDiCaL)
- **SA + peephole alternation**: SA for global restructuring, peephole for local exactness
- **GA diversity seeding**: population of structurally diverse circuits to escape local minima

See [`SOLVE_LOG.md`](SOLVE_LOG.md) for the full narrative of the LLM-assisted solve process.

### Circuit Structure
- 7 gates shared by all 9 outputs
- 8 gates dedicated to a single output
- Middle outputs (o5-o2) share 80-94% of their gates
- Sign bit (o8): 9 gates; LSB (o0): 21 gates, depends on only 6 of 8 inputs

See [`output_cone_analysis.py`](output_cone_analysis.py) for full analysis.

### Symmetry Analysis

Since `a * b = b * a`, swapping inputs `(a3,a2,a1,a0) ↔ (b3,b2,b1,b0)` must preserve all outputs. Analysis reveals the circuit already exploits this near-perfectly:

- **48 of 54 gates are symmetric** -- their truth tables are invariant under input swap
- **All 9 outputs are symmetric** (as required by commutativity)
- The 6 asymmetric gates form **3 matched swap-equivalent pairs**: `(b2|b1) ↔ (a1|a2)`, `(b0^(b2|b1)) ↔ ((a1|a2)^a0)`, and their downstream ORs
- Sorting inputs to canonicalize the pairs would cost ~14 gates but only save 3, yielding a net loss

The circuit's architecture is the natural symmetric decomposition: compute 3 "one-sided" functions per operand, then combine symmetrically. There is no remaining symmetry to exploit.

### Two Independent Circuits Converge

Two SA runs (703 and 700) independently found 54-gate circuits from different seeds and trajectories. Comparing them:

- **47 of 54 gates compute identical Boolean functions** (87% functional overlap)
- Only 7 intermediate functions differ between the circuits -- different "bridge" gates connecting the same 47 shared functions
- Gate mix: 703 uses 8 OR + 26 XOR; 700 uses 9 OR + 25 XOR (1 gate swapped)
- Critical path: 703 has depth 16; 700 has depth 17 (703 is slightly faster)
- Both have identical symmetry structure (48 symmetric + 6 asymmetric gates)

This convergence from independent trajectories strongly suggests 54 gates lies in a deep, possibly unique basin of the optimization landscape.

### Evidence of Local Optimality

- **SAT peephole windows 4-8**: exhaustive search, all UNSAT (no k→k-1 replacement exists for any connected subgraph up to size 8)
- **2 billion SA evaluations** from 54-gate seed (4 workers × 500M steps): stuck at 54
- **Symmetry exploitation**: already near-perfect, no savings available
- **Dual convergence**: two independent SA trajectories share 87% of their computation

The gap between the proven lower bound (~14-20 multi-output) and 54 remains open. Closing it would require either a fundamentally different circuit topology or a SAT proof that 53 gates is impossible.

### Mathematical Structure

Every MxFP4 magnitude decomposes as `base × 2^shift` where `base ∈ {0, 1, 3}`. This reduces FP4 multiplication to:

1. **Base extraction** (2 gates per operand): `is_three = m0 & (m1 | m2)`
2. **Base multiply** (~4 gates): `{0,1,3} × {0,1,3} → {0,1,3,9}`
3. **Shift computation** (~6 gates): add two 2-bit shift values
4. **Barrel shift** (~15-20 gates): shift base product by variable amount (the bottleneck)
5. **Sign + conditional negate** (~12 gates): `a3 XOR b3`, then two's complement
6. **Zero detection** (~2 gates): mask output when either operand is zero

The theoretical minimum from this decomposition is ~45-49 gates. The barrel shifter dominates cost because it multiplexes a 4-bit value into 8 possible positions. Our SA-found circuit likely interleaves these sub-computations, sharing gates across steps in ways a clean decomposition cannot.

## Files

| File | Description |
|------|-------------|
| `optimized_54_gates.py` | **Current best solution (54 gates)** |
| `fp4_multiplier.py` | FP4 encoding, truth tables, `verify_circuit()` |
| `output_cone_analysis.py` | Dependency cone and gate sharing analysis |
| `SOLVE_LOG.md` | Detailed log of the LLM-assisted optimization process |
| `take-home-spec.pdf` | Original problem specification |

## Running

```bash
python3 optimized_54_gates.py          # Verify the solution (256/256)
python3 output_cone_analysis.py        # Run structural analysis
```

## Output Format

```python
def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
    # 54 gates (SA-diverse-703)
    ...
    return [out8, out7, out6, out5, out4, out3, out2, out1, out0]
```
