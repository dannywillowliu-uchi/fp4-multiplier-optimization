"""
Compare the two independent 54-gate circuits (run 703 vs run 700).
Analyzes: gate type mix, depth, symmetry, shared sub-expressions, truth table equivalences.
"""

ALL = (1 << 256) - 1
def bAND(x, y): return x & y
def bOR(x, y): return x | y
def bXOR(x, y): return x ^ y
def bNOT(x): return (~x) & ALL


def make_input_tts():
	tts = {}
	names = ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]
	for row in range(256):
		a = row >> 4
		b = row & 0xF
		bits = [(a>>3)&1, (a>>2)&1, (a>>1)&1, a&1,
				(b>>3)&1, (b>>2)&1, (b>>1)&1, b&1]
		for i, v in enumerate(bits):
			tts.setdefault(names[i], 0)
			tts[names[i]] |= (v << row)
	return tts


def eval_circuit_703():
	w = make_input_tts()
	ops = []
	def g(name, op_name, val):
		w[name] = val
		ops.append((name, op_name))
		return val

	g("g0", "OR", bOR(w["b2"], w["b1"]))
	g("g1", "AND", bAND(w["b2"], w["a2"]))
	g("g2", "XOR", bXOR(w["b2"], w["a2"]))
	g("g3", "XOR", bXOR(w["b0"], w["g0"]))
	g("g4", "AND", bAND(w["a1"], w["b1"]))
	g("g5", "OR", bOR(w["a1"], w["a2"]))
	g("g6", "OR", bOR(w["a1"], w["b1"]))
	g("g7", "XOR", bXOR(w["g5"], w["a0"]))
	g("g8", "OR", bOR(w["g3"], w["g7"]))
	g("g9", "AND", bAND(w["g7"], w["g3"]))
	g("g10", "XOR", bXOR(w["a3"], w["b3"]))
	g("g11", "XOR", bXOR(w["g6"], w["g4"]))
	g("g12", "XOR", bXOR(w["g8"], w["g4"]))
	g("g13", "OR", bOR(w["g3"], w["b0"]))
	g("g14", "OR", bOR(w["g5"], w["g7"]))
	g("g15", "AND", bAND(w["g9"], w["g11"]))
	g("g16", "AND", bAND(w["g14"], w["g13"]))
	g("g17", "AND", bAND(w["g1"], w["g6"]))
	g("g18", "XOR", bXOR(w["g16"], w["g15"]))
	g("g19", "XOR", bXOR(w["g2"], w["g12"]))
	g("g20", "XOR", bXOR(w["g9"], w["g18"]))
	g("g21", "XOR", bXOR(w["g12"], w["g1"]))
	g("g22", "AND", bAND(w["g19"], w["g18"]))
	g("g23", "XOR", bXOR(w["g11"], w["g19"]))
	g("g24", "AND", bAND(w["g12"], w["g4"]))
	g("g25", "AND", bAND(w["g21"], w["g22"]))
	g("g26", "AND", bAND(w["g23"], w["g20"]))
	g("g27", "AND", bAND(w["g21"], w["g17"]))
	g("g28", "AND", bAND(w["g10"], w["g16"]))
	g("g29", "XOR", bXOR(w["g26"], w["g20"]))
	g("g30", "AND", bAND(w["g10"], w["g9"]))
	g("g31", "AND", bAND(w["g24"], w["g17"]))
	g("g32", "OR", bOR(w["g1"], w["g24"]))
	g("g33", "XOR", bXOR(w["g28"], w["g31"]))
	g("g34", "AND", bAND(w["g32"], w["g29"]))
	g("g35", "XOR", bXOR(w["g28"], w["g25"]))
	g("g36", "XOR", bXOR(w["g26"], w["g33"]))
	g("g37", "XOR", bXOR(w["g27"], w["g28"]))
	g("g38", "XOR", bXOR(w["g28"], w["g34"]))
	g("g39", "AND", bAND(w["g10"], w["g35"]))
	g("g40", "XOR", bXOR(w["g38"], w["g29"]))
	g("g41", "XOR", bXOR(w["g37"], w["g18"]))
	g("g42", "AND", bAND(w["g39"], w["g40"]))
	g("g43", "XOR", bXOR(w["g22"], w["g41"]))
	g("g44", "AND", bAND(w["g42"], w["g43"]))
	g("g45", "AND", bAND(w["g36"], w["g44"]))
	g("g46", "XOR", bXOR(w["g22"], w["g35"]))
	g("g47", "AND", bAND(w["g45"], w["g46"]))
	g("g48", "OR", bOR(w["g37"], w["g30"]))
	g("g49", "XOR", bXOR(w["g38"], w["g47"]))
	g("g50", "XOR", bXOR(w["g36"], w["g44"]))
	g("g51", "XOR", bXOR(w["g43"], w["g42"]))
	g("g52", "XOR", bXOR(w["g45"], w["g46"]))
	g("g53", "XOR", bXOR(w["g39"], w["g40"]))

	outputs = [w["g28"], w["g33"], w["g48"], w["g49"], w["g52"],
			   w["g50"], w["g51"], w["g53"], w["g25"]]
	return w, ops, outputs


def eval_circuit_700():
	w = make_input_tts()
	ops = []
	def g(name, op_name, val):
		w[name] = val
		ops.append((name, op_name))
		return val

	g("g0", "XOR", bXOR(w["b3"], w["a3"]))
	g("g1", "XOR", bXOR(w["b1"], w["a1"]))
	g("g2", "OR", bOR(w["b1"], w["b2"]))
	g("g3", "XOR", bXOR(w["b0"], w["g2"]))
	g("g4", "OR", bOR(w["g3"], w["g2"]))
	g("g5", "OR", bOR(w["a1"], w["a2"]))
	g("g6", "XOR", bXOR(w["a0"], w["g5"]))
	g("g7", "OR", bOR(w["a0"], w["g6"]))
	g("g8", "AND", bAND(w["b1"], w["a1"]))
	g("g9", "OR", bOR(w["g6"], w["g3"]))
	g("g10", "OR", bOR(w["a2"], w["b2"]))
	g("g11", "AND", bAND(w["a2"], w["b2"]))
	g("g12", "AND", bAND(w["g7"], w["g4"]))
	g("g13", "AND", bAND(w["g6"], w["g3"]))
	g("g14", "AND", bAND(w["g13"], w["g1"]))
	g("g15", "XOR", bXOR(w["g12"], w["g14"]))
	g("g16", "XOR", bXOR(w["g15"], w["g13"]))
	g("g17", "XOR", bXOR(w["g11"], w["g8"]))
	g("g18", "XOR", bXOR(w["g17"], w["g9"]))
	g("g19", "AND", bAND(w["g0"], w["g12"]))
	g("g20", "XOR", bXOR(w["g18"], w["g10"]))
	g("g21", "XOR", bXOR(w["g1"], w["g20"]))
	g("g22", "OR", bOR(w["g8"], w["g21"]))
	g("g23", "AND", bAND(w["g22"], w["g18"]))
	g("g24", "AND", bAND(w["g21"], w["g16"]))
	g("g25", "AND", bAND(w["g15"], w["g20"]))
	g("g26", "AND", bAND(w["g25"], w["g18"]))
	g("g27", "AND", bAND(w["g24"], w["g8"]))
	g("g28", "XOR", bXOR(w["g16"], w["g24"]))
	g("g29", "XOR", bXOR(w["g26"], w["g19"]))
	g("g30", "AND", bAND(w["g23"], w["g11"]))
	g("g31", "XOR", bXOR(w["g29"], w["g25"]))
	g("g32", "OR", bOR(w["g23"], w["g11"]))
	g("g33", "XOR", bXOR(w["g30"], w["g19"]))
	g("g34", "XOR", bXOR(w["g15"], w["g33"]))
	g("g35", "AND", bAND(w["g28"], w["g32"]))
	g("g36", "AND", bAND(w["g11"], w["g27"]))
	g("g37", "AND", bAND(w["g19"], w["g29"]))
	g("g38", "XOR", bXOR(w["g34"], w["g25"]))
	g("g39", "XOR", bXOR(w["g36"], w["g19"]))
	g("g40", "XOR", bXOR(w["g35"], w["g19"]))
	g("g41", "XOR", bXOR(w["g28"], w["g40"]))
	g("g42", "XOR", bXOR(w["g41"], w["g37"]))
	g("g43", "AND", bAND(w["g37"], w["g41"]))
	g("g44", "AND", bAND(w["g38"], w["g43"]))
	g("g45", "AND", bAND(w["g13"], w["g37"]))
	g("g46", "OR", bOR(w["g45"], w["g33"]))
	g("g47", "XOR", bXOR(w["g39"], w["g24"]))
	g("g48", "XOR", bXOR(w["g43"], w["g38"]))
	g("g49", "AND", bAND(w["g47"], w["g44"]))
	g("g50", "XOR", bXOR(w["g44"], w["g47"]))
	g("g51", "AND", bAND(w["g49"], w["g31"]))
	g("g52", "XOR", bXOR(w["g49"], w["g31"]))
	g("g53", "XOR", bXOR(w["g40"], w["g51"]))

	outputs = [w["g19"], w["g39"], w["g46"], w["g53"], w["g52"],
			   w["g50"], w["g48"], w["g42"], w["g26"]]
	return w, ops, outputs


def compute_depth(gate_defs_703, gate_defs_700):
	"""Compute critical path depth for each circuit."""
	# Circuit 703
	deps_703 = {
		"g0": ["b2", "b1"], "g1": ["b2", "a2"], "g2": ["b2", "a2"],
		"g3": ["b0", "g0"], "g4": ["a1", "b1"], "g5": ["a1", "a2"],
		"g6": ["a1", "b1"], "g7": ["g5", "a0"], "g8": ["g3", "g7"],
		"g9": ["g7", "g3"], "g10": ["a3", "b3"], "g11": ["g6", "g4"],
		"g12": ["g8", "g4"], "g13": ["g3", "b0"], "g14": ["g5", "g7"],
		"g15": ["g9", "g11"], "g16": ["g14", "g13"], "g17": ["g1", "g6"],
		"g18": ["g16", "g15"], "g19": ["g2", "g12"], "g20": ["g9", "g18"],
		"g21": ["g12", "g1"], "g22": ["g19", "g18"], "g23": ["g11", "g19"],
		"g24": ["g12", "g4"], "g25": ["g21", "g22"], "g26": ["g23", "g20"],
		"g27": ["g21", "g17"], "g28": ["g10", "g16"], "g29": ["g26", "g20"],
		"g30": ["g10", "g9"], "g31": ["g24", "g17"], "g32": ["g1", "g24"],
		"g33": ["g28", "g31"], "g34": ["g32", "g29"], "g35": ["g28", "g25"],
		"g36": ["g26", "g33"], "g37": ["g27", "g28"], "g38": ["g28", "g34"],
		"g39": ["g10", "g35"], "g40": ["g38", "g29"], "g41": ["g37", "g18"],
		"g42": ["g39", "g40"], "g43": ["g22", "g41"], "g44": ["g42", "g43"],
		"g45": ["g36", "g44"], "g46": ["g22", "g35"], "g47": ["g45", "g46"],
		"g48": ["g37", "g30"], "g49": ["g38", "g47"], "g50": ["g36", "g44"],
		"g51": ["g43", "g42"], "g52": ["g45", "g46"], "g53": ["g39", "g40"],
	}

	deps_700 = {
		"g0": ["b3", "a3"], "g1": ["b1", "a1"], "g2": ["b1", "b2"],
		"g3": ["b0", "g2"], "g4": ["g3", "g2"], "g5": ["a1", "a2"],
		"g6": ["a0", "g5"], "g7": ["a0", "g6"], "g8": ["b1", "a1"],
		"g9": ["g6", "g3"], "g10": ["a2", "b2"], "g11": ["a2", "b2"],
		"g12": ["g7", "g4"], "g13": ["g6", "g3"], "g14": ["g13", "g1"],
		"g15": ["g12", "g14"], "g16": ["g15", "g13"], "g17": ["g11", "g8"],
		"g18": ["g17", "g9"], "g19": ["g0", "g12"], "g20": ["g18", "g10"],
		"g21": ["g1", "g20"], "g22": ["g8", "g21"], "g23": ["g22", "g18"],
		"g24": ["g21", "g16"], "g25": ["g15", "g20"], "g26": ["g25", "g18"],
		"g27": ["g24", "g8"], "g28": ["g16", "g24"], "g29": ["g26", "g19"],
		"g30": ["g23", "g11"], "g31": ["g29", "g25"], "g32": ["g23", "g11"],
		"g33": ["g30", "g19"], "g34": ["g15", "g33"], "g35": ["g28", "g32"],
		"g36": ["g11", "g27"], "g37": ["g19", "g29"], "g38": ["g34", "g25"],
		"g39": ["g36", "g19"], "g40": ["g35", "g19"], "g41": ["g28", "g40"],
		"g42": ["g41", "g37"], "g43": ["g37", "g41"], "g44": ["g38", "g43"],
		"g45": ["g13", "g37"], "g46": ["g45", "g33"], "g47": ["g39", "g24"],
		"g48": ["g43", "g38"], "g49": ["g47", "g44"], "g50": ["g44", "g47"],
		"g51": ["g49", "g31"], "g52": ["g49", "g31"], "g53": ["g40", "g51"],
	}

	inputs = {"a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"}

	def get_depth(deps_map):
		depth = {inp: 0 for inp in inputs}
		for gname in [f"g{i}" for i in range(54)]:
			d = max(depth.get(p, 0) for p in deps_map[gname]) + 1
			depth[gname] = d
		return depth

	d703 = get_depth(deps_703)
	d700 = get_depth(deps_700)

	outs_703 = ["g28", "g33", "g48", "g49", "g52", "g50", "g51", "g53", "g25"]
	outs_700 = ["g19", "g39", "g46", "g53", "g52", "g50", "g48", "g42", "g26"]

	return d703, outs_703, d700, outs_700


def main():
	w703, ops703, out703 = eval_circuit_703()
	w700, ops700, out700 = eval_circuit_700()

	print("=" * 70)
	print("Comparison: 54-gate Circuit Run 703 vs Run 700")
	print("=" * 70)

	# Verify both produce same outputs
	print("\n--- Output verification ---")
	for i in range(9):
		match = "MATCH" if out703[i] == out700[i] else "DIFFER"
		print(f"  out[{i}]: {match}")

	# Gate type mix
	print("\n--- Gate type mix ---")
	for name, ops_list in [("Run 703", ops703), ("Run 700", ops700)]:
		counts = {"AND": 0, "OR": 0, "XOR": 0, "NOT": 0}
		for _, op in ops_list:
			counts[op] += 1
		print(f"  {name}: {counts}")

	# Truth table comparison: how many gates compute the same function?
	print("\n--- Truth table equivalences ---")
	tt_to_gates_703 = {}
	for gname, _ in ops703:
		tt = w703[gname]
		tt_to_gates_703.setdefault(tt, []).append(f"703:{gname}")

	tt_to_gates_700 = {}
	for gname, _ in ops700:
		tt = w700[gname]
		tt_to_gates_700.setdefault(tt, []).append(f"700:{gname}")

	# Find TTs that appear in both circuits
	shared_tts = set(tt_to_gates_703.keys()) & set(tt_to_gates_700.keys())
	only_703 = set(tt_to_gates_703.keys()) - set(tt_to_gates_700.keys())
	only_700 = set(tt_to_gates_700.keys()) - set(tt_to_gates_703.keys())

	print(f"  Unique truth tables in 703: {len(tt_to_gates_703)}")
	print(f"  Unique truth tables in 700: {len(tt_to_gates_700)}")
	print(f"  Shared (same function computed): {len(shared_tts)}")
	print(f"  Only in 703: {len(only_703)}")
	print(f"  Only in 700: {len(only_700)}")

	print(f"\n  Shared functions:")
	for tt in shared_tts:
		g703 = tt_to_gates_703[tt]
		g700 = tt_to_gates_700[tt]
		print(f"    {g703} == {g700}")

	# Also check complements (NOT of each other)
	complement_matches = 0
	for tt703 in tt_to_gates_703:
		comp = (~tt703) & ALL
		if comp in tt_to_gates_700:
			complement_matches += 1

	print(f"\n  Complement matches (703 gate == NOT of 700 gate): {complement_matches}")

	# Depth analysis
	print("\n--- Critical path depth ---")
	d703, outs703, d700, outs700 = compute_depth(None, None)

	print(f"  Run 703:")
	max_d = 0
	for i, oname in enumerate(outs703):
		d = d703[oname]
		max_d = max(max_d, d)
		print(f"    out[{i}] ({oname}): depth {d}")
	print(f"    Max depth: {max_d}")

	print(f"  Run 700:")
	max_d = 0
	for i, oname in enumerate(outs700):
		d = d700[oname]
		max_d = max(max_d, d)
		print(f"    out[{i}] ({oname}): depth {d}")
	print(f"    Max depth: {max_d}")

	# Symmetry comparison
	print("\n--- Symmetry under a<->b swap ---")
	swap_perm = {}
	for row in range(256):
		a = row >> 4
		b = row & 0xF
		swap_perm[row] = (b << 4) | a

	def permute_tt(tt):
		result = 0
		for row in range(256):
			result |= (((tt >> row) & 1) << swap_perm[row])
		return result

	for name, wire, ops_list in [("703", w703, ops703), ("700", w700, ops700)]:
		sym = asym = 0
		for gname, _ in ops_list:
			swapped = permute_tt(wire[gname])
			if swapped == wire[gname]:
				sym += 1
			else:
				asym += 1
		print(f"  Run {name}: {sym} symmetric, {asym} asymmetric")

	# What sub-expressions are different?
	print("\n--- Structural differences ---")
	# Count which primary inputs each circuit uses in its first few gates
	print("  Run 703 early gates (first interaction with inputs):")
	for gname, op in ops703[:14]:
		print(f"    {gname} = {op}")

	print("  Run 700 early gates:")
	for gname, op in ops700[:14]:
		print(f"    {gname} = {op}")


if __name__ == "__main__":
	main()
