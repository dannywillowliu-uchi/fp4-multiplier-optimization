"""
Analyze each output bit's dependency cone in the 54-gate circuit.
Identify which gates are shared vs. dedicated to each output.

Circuit: 54 gates (20 AND + 8 OR + 26 XOR + 0 NOT)
Source: SA-diverse run 703 (sa_from_56.py), found at step 16,730,506
        from 56-gate seed circuit, T=30, cooling=0.9999970
Also found independently by SA-diverse run 700 at step 269,354,924
"""
import sys
sys.path.insert(0, "/Users/dannyliu/personal_projects/etched_problem")
from fp4_multiplier import generate_truth_table


def parse_circuit_54():
	"""Parse 54-gate circuit into structured form."""
	inputs = ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]
	gates = [
		("g0", "|", "b2", "b1"), ("g1", "&", "b2", "a2"), ("g2", "^", "b2", "a2"),
		("g3", "^", "b0", "g0"), ("g4", "&", "a1", "b1"), ("g5", "|", "a1", "a2"),
		("g6", "|", "a1", "b1"), ("g7", "^", "g5", "a0"), ("g8", "|", "g3", "g7"),
		("g9", "&", "g7", "g3"), ("g10", "^", "a3", "b3"), ("g11", "^", "g6", "g4"),
		("g12", "^", "g8", "g4"), ("g13", "|", "g3", "b0"), ("g14", "|", "g5", "g7"),
		("g15", "&", "g9", "g11"), ("g16", "&", "g14", "g13"), ("g17", "&", "g1", "g6"),
		("g18", "^", "g16", "g15"), ("g19", "^", "g2", "g12"), ("g20", "^", "g9", "g18"),
		("g21", "^", "g12", "g1"), ("g22", "&", "g19", "g18"), ("g23", "^", "g11", "g19"),
		("g24", "&", "g12", "g4"), ("g25", "&", "g21", "g22"), ("g26", "&", "g23", "g20"),
		("g27", "&", "g21", "g17"), ("g28", "&", "g10", "g16"), ("g29", "^", "g26", "g20"),
		("g30", "&", "g10", "g9"), ("g31", "&", "g24", "g17"), ("g32", "|", "g1", "g24"),
		("g33", "^", "g28", "g31"), ("g34", "&", "g32", "g29"), ("g35", "^", "g28", "g25"),
		("g36", "^", "g26", "g33"), ("g37", "^", "g27", "g28"), ("g38", "^", "g28", "g34"),
		("g39", "&", "g10", "g35"), ("g40", "^", "g38", "g29"), ("g41", "^", "g37", "g18"),
		("g42", "&", "g39", "g40"), ("g43", "^", "g22", "g41"), ("g44", "&", "g42", "g43"),
		("g45", "&", "g36", "g44"), ("g46", "^", "g22", "g35"), ("g47", "&", "g45", "g46"),
		("g48", "|", "g37", "g30"), ("g49", "^", "g38", "g47"), ("g50", "^", "g36", "g44"),
		("g51", "^", "g43", "g42"), ("g52", "^", "g45", "g46"), ("g53", "^", "g39", "g40"),
	]
	outputs = {
		"o8": "g28", "o7": "g33", "o6": "g48", "o5": "g49",
		"o4": "g52", "o3": "g50", "o2": "g51", "o1": "g53", "o0": "g25"
	}
	return inputs, gates, outputs


def compute_dependency_cones():
	"""For each output, find which gates it depends on."""
	inputs, gates, outputs = parse_circuit_54()

	# Build wire->gate_index mapping
	wire_to_idx = {}
	for i, name in enumerate(["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]):
		wire_to_idx[name] = -1  # inputs

	gate_map = {}
	for i, (name, op, in1, in2) in enumerate(gates):
		wire_to_idx[name] = i
		gate_map[name] = (op, in1, in2)

	def get_cone(wire, visited=None):
		"""Get all gate indices in the dependency cone of a wire."""
		if visited is None:
			visited = set()
		if wire in visited:
			return set()
		visited.add(wire)
		idx = wire_to_idx.get(wire, -1)
		if idx < 0:
			return set()
		op, in1, in2 = gates[idx][1], gates[idx][2], gates[idx][3]
		cone = {idx}
		cone |= get_cone(in1, visited)
		cone |= get_cone(in2, visited)
		return cone

	# Compute cones for each output
	print("=== Output Dependency Cones ===\n")
	cones = {}
	for out_name in ["o8", "o7", "o6", "o5", "o4", "o3", "o2", "o1", "o0"]:
		wire = outputs[out_name]
		cone = get_cone(wire)
		cones[out_name] = cone

		# Find which inputs this output depends on
		dep_inputs = set()
		for gi in cone:
			gname, op, in1, in2 = gates[gi]
			if in1 in ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]:
				dep_inputs.add(in1)
			if in2 in ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]:
				dep_inputs.add(in2)

		gate_types = {}
		for gi in cone:
			op = gates[gi][1]
			gate_types[op] = gate_types.get(op, 0) + 1

		print(f"{out_name} ({wire}): {len(cone)} gates, depends on {sorted(dep_inputs)}")
		print(f"  Gate types: {gate_types}")

	# Sharing analysis
	print("\n=== Gate Sharing Matrix ===\n")
	print(f"{'Gate':<5}", end="")
	for out_name in ["o8", "o7", "o6", "o5", "o4", "o3", "o2", "o1", "o0"]:
		print(f" {out_name}", end="")
	print("  #outs")

	for gi in range(len(gates)):
		gname = gates[gi][0]
		used_by = []
		for out_name in ["o8", "o7", "o6", "o5", "o4", "o3", "o2", "o1", "o0"]:
			if gi in cones[out_name]:
				used_by.append(out_name)

		n_outs = len(used_by)
		if n_outs == 0:
			continue  # dead gate

		print(f"{gname:<5}", end="")
		for out_name in ["o8", "o7", "o6", "o5", "o4", "o3", "o2", "o1", "o0"]:
			if gi in cones[out_name]:
				print(f"  X", end="")
			else:
				print(f"  .", end="")
		print(f"  {n_outs}")

	# Summary: gates shared by N outputs
	print("\n=== Sharing Summary ===\n")
	sharing = {}
	for gi in range(len(gates)):
		n = sum(1 for cn in cones.values() if gi in cn)
		sharing[n] = sharing.get(n, 0) + 1

	for n in sorted(sharing.keys()):
		print(f"  Gates used by {n} output(s): {sharing[n]}")

	# Union of cones vs total gates
	all_used = set()
	for cn in cones.values():
		all_used |= cn
	print(f"\n  Total gates used: {len(all_used)} / {len(gates)}")

	# Output pairs that share the most gates
	print("\n=== Pairwise Sharing ===\n")
	out_names = ["o8", "o7", "o6", "o5", "o4", "o3", "o2", "o1", "o0"]
	for i in range(len(out_names)):
		for j in range(i+1, len(out_names)):
			shared = len(cones[out_names[i]] & cones[out_names[j]])
			union = len(cones[out_names[i]] | cones[out_names[j]])
			print(f"  {out_names[i]},{out_names[j]}: shared={shared}/{union} ({100*shared/union:.0f}%)")

	return cones, gates, outputs


def analyze_truth_tables():
	"""Analyze each output's truth table properties."""
	table = generate_truth_table()

	print("\n=== Output Truth Table Analysis ===\n")
	for out_idx in range(9):
		out_name = f"o{8-out_idx}"
		col = table[:, 8 + out_idx]
		weight = int(col.sum())

		# Count how many of the 256 outputs are 1
		# Sensitivity: how many bits change when one input bit flips
		sensitivity = 0
		for bit in range(8):
			for row in range(256):
				partner = row ^ (1 << bit)
				if col[row] != col[partner]:
					sensitivity += 1
		avg_sensitivity = sensitivity / (256 * 8)

		# Nonlinearity: distance from nearest affine function
		# (requires Walsh transform - skip for now)

		print(f"{out_name}: weight={weight}/256 ({100*weight/256:.1f}%), avg_sensitivity={avg_sensitivity:.3f}")


if __name__ == "__main__":
	print("=" * 60)
	print("54-Gate Circuit: Output Cone Analysis")
	print("=" * 60)

	cones, gates, outputs = compute_dependency_cones()
	analyze_truth_tables()
