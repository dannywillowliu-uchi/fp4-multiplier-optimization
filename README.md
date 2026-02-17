# FP4 Multiplier Optimization

## Problem Summary
Design a minimum-gate-count circuit for multiplying two 4-bit FP4 (MxFP4) numbers, outputting `(a * b * 4)` as a 9-bit two's complement integer.

### Constraints
- Gates: XOR, AND, OR (2-input), NOT (1-input) - each costs 1 gate
- Free: constants (0, 1), input remapping (same mapping for both inputs)
- Cannot remap output

## Current Best: 54 Gates

**20 AND + 8 OR + 26 XOR + 0 NOT = 54 gates** -- verified 256/256 correct.

Found by SA-diverse run 703 from a 56-gate seed at step 16,730,506 (T=30, cooling=0.9999970).
Also found independently by run 700 at step 269,354,924 with a different gate topology.

See `optimized_54_gates.py` for the circuit implementation.

### Optimization History
```
205 -> 87 -> 83 -> 77 -> 73 -> 71 -> 69 -> 67 -> 66 -> 65 -> 64 -> 63 -> 62 -> 61 -> 60 -> 59 -> 58 -> 57 -> 56 -> 54
```

Key techniques used in cascade:
- **Hand-crafted structural decomposition** (205 -> 87)
- **CGP (Cartesian Genetic Programming)** (87 -> 83)
- **Simulated annealing on DAG** (83 -> 77 -> ... -> 57)
- **SAT peephole optimization** (local k-gate window replacement via SAT solver)
- **SA + peephole alternation** (breaks through local minima)
- **Structural diversity** (GA population for diverse seeds)

### Circuit Structure (54 gates)
- 7 gates shared by all 9 outputs (core logic)
- Only 8 gates dedicated to a single output
- Middle outputs (o5-o2) share 80-94% of their gates
- Sign bit (o8) needs only 9 gates
- LSB (o0) depends on only 6 of 8 inputs

See `output_cone_analysis.py` for full sharing/dependency analysis.

### Lower Bounds
- Per-bit independent lower bound: 67 gates (SAT-proven)
- Current circuit beats this by 13 gates (proves inter-output sharing saves 13+ gates)
- True multi-output lower bound: unknown (SAT intractable for full 9-output problem)

## Files

| File | Description |
|------|-------------|
| `optimized_54_gates.py` | **Current best solution (54 gates)** |
| `fp4_multiplier.py` | FP4 encoding, truth tables, `verify_circuit()` |
| `output_cone_analysis.py` | Dependency cone and gate sharing analysis for the 54-gate circuit |

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
