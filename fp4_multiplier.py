"""
FP4 Multiplier - Core utilities for FP4 encoding and truth table generation.

FP4 Format (MxFP4):
- 4-bit encoding for floating point values
- 16 values: 0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6
- Output: (a × b × 4) as 9-bit two's complement integer
"""

from typing import Dict, List, Tuple
import numpy as np


# Default FP4 encoding from the problem spec
DEFAULT_FP4_VALUES = {
	0b0000: 0.0,
	0b0001: 0.5,
	0b0010: 1.0,
	0b0011: 1.5,
	0b0100: 2.0,
	0b0101: 3.0,
	0b0110: 4.0,
	0b0111: 6.0,
	0b1000: 0.0,   # Negative zero (treated as zero)
	0b1001: -0.5,
	0b1010: -1.0,
	0b1011: -1.5,
	0b1100: -2.0,
	0b1101: -3.0,
	0b1110: -4.0,
	0b1111: -6.0,
}


def to_twos_complement(value: int, bits: int = 9) -> int:
	"""Convert signed integer to two's complement representation."""
	if value < 0:
		return (1 << bits) + value
	return value


def from_twos_complement(value: int, bits: int = 9) -> int:
	"""Convert two's complement to signed integer."""
	if value >= (1 << (bits - 1)):
		return value - (1 << bits)
	return value


def fp4_multiply(a_val: float, b_val: float) -> float:
	"""Multiply two FP4 values and return result × 4."""
	return a_val * b_val * 4


def generate_truth_table(encoding: Dict[int, float] = None) -> np.ndarray:
	"""
	Generate complete 256-entry truth table.

	Returns:
		np.ndarray of shape (256, 17):
		- Columns 0-3: input a bits (a3, a2, a1, a0)
		- Columns 4-7: input b bits (b3, b2, b1, b0)
		- Columns 8-16: output bits (o8, o7, ..., o0) in two's complement
	"""
	if encoding is None:
		encoding = DEFAULT_FP4_VALUES

	table = np.zeros((256, 17), dtype=np.int8)

	for a in range(16):
		for b in range(16):
			idx = a * 16 + b

			# Input bits
			table[idx, 0] = (a >> 3) & 1  # a3
			table[idx, 1] = (a >> 2) & 1  # a2
			table[idx, 2] = (a >> 1) & 1  # a1
			table[idx, 3] = a & 1          # a0
			table[idx, 4] = (b >> 3) & 1  # b3
			table[idx, 5] = (b >> 2) & 1  # b2
			table[idx, 6] = (b >> 1) & 1  # b1
			table[idx, 7] = b & 1          # b0

			# Compute product × 4
			a_val = encoding[a]
			b_val = encoding[b]
			product_x4 = int(a_val * b_val * 4)

			# Convert to 9-bit two's complement
			tc = to_twos_complement(product_x4, 9)

			# Output bits (MSB to LSB)
			for i in range(9):
				table[idx, 8 + i] = (tc >> (8 - i)) & 1

	return table


def get_output_for_inputs(a: int, b: int, encoding: Dict[int, float] = None) -> Tuple[int, int]:
	"""
	Get the expected output for given inputs.

	Returns:
		Tuple of (signed_value, unsigned_twos_complement)
	"""
	if encoding is None:
		encoding = DEFAULT_FP4_VALUES

	a_val = encoding[a]
	b_val = encoding[b]
	product_x4 = int(a_val * b_val * 4)
	tc = to_twos_complement(product_x4, 9)

	return product_x4, tc


def analyze_truth_table(table: np.ndarray) -> Dict:
	"""Analyze the truth table for useful patterns."""

	# Extract output columns
	outputs = table[:, 8:]

	# Convert to integers
	output_ints = np.zeros(256, dtype=np.int32)
	for i in range(256):
		val = 0
		for j in range(9):
			val = (val << 1) | outputs[i, j]
		output_ints[i] = val

	# Unique outputs
	unique_outputs = np.unique(output_ints)

	# Per-bit analysis
	bit_stats = []
	for bit in range(9):
		ones = np.sum(outputs[:, bit])
		zeros = 256 - ones
		bit_stats.append({
			"bit": 8 - bit,
			"ones": int(ones),
			"zeros": int(zeros),
		})

	# Zero detection (both 0000 and 1000 are zero)
	zero_inputs = []
	for a in range(16):
		for b in range(16):
			idx = a * 16 + b
			if output_ints[idx] == 0:
				zero_inputs.append((a, b))

	return {
		"unique_outputs": len(unique_outputs),
		"unique_output_values": sorted([from_twos_complement(v) for v in unique_outputs]),
		"bit_stats": bit_stats,
		"zero_input_count": len(zero_inputs),
	}


def print_truth_table(table: np.ndarray, encoding: Dict[int, float] = None):
	"""Print truth table in readable format."""
	if encoding is None:
		encoding = DEFAULT_FP4_VALUES

	print("a    | b    | a_val | b_val | prod*4 | output (bin)")
	print("-" * 60)

	for i in range(256):
		a = i // 16
		b = i % 16

		a_bits = f"{a:04b}"
		b_bits = f"{b:04b}"
		a_val = encoding[a]
		b_val = encoding[b]
		prod = int(a_val * b_val * 4)

		out_bits = "".join(str(table[i, 8 + j]) for j in range(9))

		print(f"{a_bits} | {b_bits} | {a_val:5.1f} | {b_val:5.1f} | {prod:6d} | {out_bits}")


def verify_circuit(circuit_fn, encoding: Dict[int, float] = None, remap: Dict[int, int] = None) -> Tuple[bool, List]:
	"""
	Verify a circuit implementation against the truth table.

	Args:
		circuit_fn: Function that takes (a3,a2,a1,a0,b3,b2,b1,b0) and returns 9 output bits
		encoding: FP4 value mapping
		remap: Input remapping (original_code -> remapped_code)

	Returns:
		Tuple of (success, list of failures)
	"""
	if encoding is None:
		encoding = DEFAULT_FP4_VALUES
	if remap is None:
		remap = {i: i for i in range(16)}

	failures = []

	for a_orig in range(16):
		for b_orig in range(16):
			# Apply remapping
			a = remap[a_orig]
			b = remap[b_orig]

			# Get expected output
			expected_signed, expected_tc = get_output_for_inputs(a_orig, b_orig, encoding)

			# Get circuit output
			a_bits = [(a >> (3 - i)) & 1 for i in range(4)]
			b_bits = [(b >> (3 - i)) & 1 for i in range(4)]

			try:
				output = circuit_fn(*a_bits, *b_bits)
				if isinstance(output, (list, tuple)):
					actual = 0
					for bit in output:
						actual = (actual << 1) | int(bit)
				else:
					actual = int(output)
			except Exception as e:
				failures.append((a_orig, b_orig, f"Error: {e}"))
				continue

			if actual != expected_tc:
				failures.append((a_orig, b_orig, f"Expected {expected_tc:09b}, got {actual:09b}"))

	return len(failures) == 0, failures


if __name__ == "__main__":
	print("FP4 Multiplier Truth Table Analysis")
	print("=" * 60)

	table = generate_truth_table()
	analysis = analyze_truth_table(table)

	print(f"\nTotal entries: 256")
	print(f"Unique outputs: {analysis['unique_outputs']}")
	print(f"Zero input combinations: {analysis['zero_input_count']}")

	print("\nBit statistics (ones/zeros):")
	for stat in analysis['bit_stats']:
		print(f"  Bit {stat['bit']}: {stat['ones']} ones, {stat['zeros']} zeros")

	print("\nUnique output values (product × 4):")
	print(analysis['unique_output_values'])

	print("\nSample entries (first 10):")
	for i in range(10):
		a = i // 16
		b = i % 16
		a_bits = f"{a:04b}"
		b_bits = f"{b:04b}"
		a_val = DEFAULT_FP4_VALUES[a]
		b_val = DEFAULT_FP4_VALUES[b]
		prod = int(a_val * b_val * 4)
		out_bits = "".join(str(table[i, 8 + j]) for j in range(9))
		print(f"{a_bits} | {b_bits} | {a_val:5.1f} | {b_val:5.1f} | {prod:6d} | {out_bits}")
