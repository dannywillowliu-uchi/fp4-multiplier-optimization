"""
Commutativity analysis of the 54-gate circuit.

Since a*b = b*a, swapping inputs (a3,a2,a1,a0) <-> (b3,b2,b1,b0) should
produce the same outputs. This means:
1. Some gates may compute identical functions under swap
2. A "symmetric" circuit could share these, potentially saving gates
3. We can quantify how much symmetry the current circuit exploits

Approach: Evaluate every gate's truth table under both normal and swapped inputs.
If gate_i(a,b) == gate_j(b,a), they're "swap-equivalent" and only one is needed.
"""

import sys
sys.path.insert(0, ".")


def evaluate_all_tts():
	"""Compute 256-bit truth table for every wire in the 54-gate circuit."""
	# Input truth tables (256 rows)
	tts = {}
	for row in range(256):
		a = row >> 4
		b = row & 0xF
		a3, a2, a1, a0 = (a >> 3) & 1, (a >> 2) & 1, (a >> 1) & 1, a & 1
		b3, b2, b1, b0 = (b >> 3) & 1, (b >> 2) & 1, (b >> 1) & 1, b & 1
		for i, v in enumerate([a3, a2, a1, a0, b3, b2, b1, b0]):
			tts.setdefault(f"in{i}", 0)
			tts[f"in{i}"] |= (v << row)

	names = ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]
	wire = {names[i]: tts[f"in{i}"] for i in range(8)}
	ALL = (1 << 256) - 1

	def AND(x, y): return x & y
	def OR(x, y): return x | y
	def XOR(x, y): return x ^ y
	def NOT(x): return (~x) & ALL

	# Gate definitions from the circuit
	gates = []
	def g(name, val):
		wire[name] = val
		gates.append(name)
		return val

	g("g0", OR(wire["b2"], wire["b1"]))
	g("g1", AND(wire["b2"], wire["a2"]))
	g("g2", XOR(wire["b2"], wire["a2"]))
	g("g3", XOR(wire["b0"], wire["g0"]))
	g("g4", AND(wire["a1"], wire["b1"]))
	g("g5", OR(wire["a1"], wire["a2"]))
	g("g6", OR(wire["a1"], wire["b1"]))
	g("g7", XOR(wire["g5"], wire["a0"]))
	g("g8", OR(wire["g3"], wire["g7"]))
	g("g9", AND(wire["g7"], wire["g3"]))
	g("g10", XOR(wire["a3"], wire["b3"]))
	g("g11", XOR(wire["g6"], wire["g4"]))
	g("g12", XOR(wire["g8"], wire["g4"]))
	g("g13", OR(wire["g3"], wire["b0"]))
	g("g14", OR(wire["g5"], wire["g7"]))
	g("g15", AND(wire["g9"], wire["g11"]))
	g("g16", AND(wire["g14"], wire["g13"]))
	g("g17", AND(wire["g1"], wire["g6"]))
	g("g18", XOR(wire["g16"], wire["g15"]))
	g("g19", XOR(wire["g2"], wire["g12"]))
	g("g20", XOR(wire["g9"], wire["g18"]))
	g("g21", XOR(wire["g12"], wire["g1"]))
	g("g22", AND(wire["g19"], wire["g18"]))
	g("g23", XOR(wire["g11"], wire["g19"]))
	g("g24", AND(wire["g12"], wire["g4"]))
	g("g25", AND(wire["g21"], wire["g22"]))
	g("g26", AND(wire["g23"], wire["g20"]))
	g("g27", AND(wire["g21"], wire["g17"]))
	g("g28", AND(wire["g10"], wire["g16"]))
	g("g29", XOR(wire["g26"], wire["g20"]))
	g("g30", AND(wire["g10"], wire["g9"]))
	g("g31", AND(wire["g24"], wire["g17"]))
	g("g32", OR(wire["g1"], wire["g24"]))
	g("g33", XOR(wire["g28"], wire["g31"]))
	g("g34", AND(wire["g32"], wire["g29"]))
	g("g35", XOR(wire["g28"], wire["g25"]))
	g("g36", XOR(wire["g26"], wire["g33"]))
	g("g37", XOR(wire["g27"], wire["g28"]))
	g("g38", XOR(wire["g28"], wire["g34"]))
	g("g39", AND(wire["g10"], wire["g35"]))
	g("g40", XOR(wire["g38"], wire["g29"]))
	g("g41", XOR(wire["g37"], wire["g18"]))
	g("g42", AND(wire["g39"], wire["g40"]))
	g("g43", XOR(wire["g22"], wire["g41"]))
	g("g44", AND(wire["g42"], wire["g43"]))
	g("g45", AND(wire["g36"], wire["g44"]))
	g("g46", XOR(wire["g22"], wire["g35"]))
	g("g47", AND(wire["g45"], wire["g46"]))
	g("g48", OR(wire["g37"], wire["g30"]))
	g("g49", XOR(wire["g38"], wire["g47"]))
	g("g50", XOR(wire["g36"], wire["g44"]))
	g("g51", XOR(wire["g43"], wire["g42"]))
	g("g52", XOR(wire["g45"], wire["g46"]))
	g("g53", XOR(wire["g39"], wire["g40"]))

	return wire, gates


def evaluate_swapped_tts():
	"""Same circuit but with a<->b swapped at input."""
	tts = {}
	for row in range(256):
		a = row >> 4
		b = row & 0xF
		a3, a2, a1, a0 = (a >> 3) & 1, (a >> 2) & 1, (a >> 1) & 1, a & 1
		b3, b2, b1, b0 = (b >> 3) & 1, (b >> 2) & 1, (b >> 1) & 1, b & 1
		# SWAP: feed b as 'a' and a as 'b'
		for i, v in enumerate([b3, b2, b1, b0, a3, a2, a1, a0]):
			tts.setdefault(f"in{i}", 0)
			tts[f"in{i}"] |= (v << row)

	names = ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]
	wire = {names[i]: tts[f"in{i}"] for i in range(8)}
	ALL = (1 << 256) - 1

	def AND(x, y): return x & y
	def OR(x, y): return x | y
	def XOR(x, y): return x ^ y

	gates = []
	def g(name, val):
		wire[name] = val
		gates.append(name)
		return val

	# Same circuit structure
	g("g0", OR(wire["b2"], wire["b1"]))
	g("g1", AND(wire["b2"], wire["a2"]))
	g("g2", XOR(wire["b2"], wire["a2"]))
	g("g3", XOR(wire["b0"], wire["g0"]))
	g("g4", AND(wire["a1"], wire["b1"]))
	g("g5", OR(wire["a1"], wire["a2"]))
	g("g6", OR(wire["a1"], wire["b1"]))
	g("g7", XOR(wire["g5"], wire["a0"]))
	g("g8", OR(wire["g3"], wire["g7"]))
	g("g9", AND(wire["g7"], wire["g3"]))
	g("g10", XOR(wire["a3"], wire["b3"]))
	g("g11", XOR(wire["g6"], wire["g4"]))
	g("g12", XOR(wire["g8"], wire["g4"]))
	g("g13", OR(wire["g3"], wire["b0"]))
	g("g14", OR(wire["g5"], wire["g7"]))
	g("g15", AND(wire["g9"], wire["g11"]))
	g("g16", AND(wire["g14"], wire["g13"]))
	g("g17", AND(wire["g1"], wire["g6"]))
	g("g18", XOR(wire["g16"], wire["g15"]))
	g("g19", XOR(wire["g2"], wire["g12"]))
	g("g20", XOR(wire["g9"], wire["g18"]))
	g("g21", XOR(wire["g12"], wire["g1"]))
	g("g22", AND(wire["g19"], wire["g18"]))
	g("g23", XOR(wire["g11"], wire["g19"]))
	g("g24", AND(wire["g12"], wire["g4"]))
	g("g25", AND(wire["g21"], wire["g22"]))
	g("g26", AND(wire["g23"], wire["g20"]))
	g("g27", AND(wire["g21"], wire["g17"]))
	g("g28", AND(wire["g10"], wire["g16"]))
	g("g29", XOR(wire["g26"], wire["g20"]))
	g("g30", AND(wire["g10"], wire["g9"]))
	g("g31", AND(wire["g24"], wire["g17"]))
	g("g32", OR(wire["g1"], wire["g24"]))
	g("g33", XOR(wire["g28"], wire["g31"]))
	g("g34", AND(wire["g32"], wire["g29"]))
	g("g35", XOR(wire["g28"], wire["g25"]))
	g("g36", XOR(wire["g26"], wire["g33"]))
	g("g37", XOR(wire["g27"], wire["g28"]))
	g("g38", XOR(wire["g28"], wire["g34"]))
	g("g39", AND(wire["g10"], wire["g35"]))
	g("g40", XOR(wire["g38"], wire["g29"]))
	g("g41", XOR(wire["g37"], wire["g18"]))
	g("g42", AND(wire["g39"], wire["g40"]))
	g("g43", XOR(wire["g22"], wire["g41"]))
	g("g44", AND(wire["g42"], wire["g43"]))
	g("g45", AND(wire["g36"], wire["g44"]))
	g("g46", XOR(wire["g22"], wire["g35"]))
	g("g47", AND(wire["g45"], wire["g46"]))
	g("g48", OR(wire["g37"], wire["g30"]))
	g("g49", XOR(wire["g38"], wire["g47"]))
	g("g50", XOR(wire["g36"], wire["g44"]))
	g("g51", XOR(wire["g43"], wire["g42"]))
	g("g52", XOR(wire["g45"], wire["g46"]))
	g("g53", XOR(wire["g39"], wire["g40"]))

	return wire, gates


def build_swap_permutation():
	"""Build the row permutation that swaps a<->b.
	Row r = (a<<4)|b maps to row r' = (b<<4)|a."""
	perm = {}
	for row in range(256):
		a = row >> 4
		b = row & 0xF
		perm[row] = (b << 4) | a
	return perm


def permute_tt(tt, perm):
	"""Given a 256-bit truth table and a row permutation, return permuted tt."""
	result = 0
	for row in range(256):
		bit = (tt >> row) & 1
		result |= (bit << perm[row])
	return result


def main():
	wire_normal, gates = evaluate_all_tts()
	swap_perm = build_swap_permutation()

	print("=" * 70)
	print("Commutativity Analysis of 54-gate Circuit")
	print("=" * 70)

	# For each gate, compute its truth table under swap
	# gate_normal[i] = tt when inputs are (a,b)
	# gate_swapped[i] = tt when inputs are (b,a) = permute_tt(gate_normal[i], swap_perm)
	print("\n--- Gate truth tables under input swap ---")

	all_names = ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"] + gates
	normal_tts = {name: wire_normal[name] for name in all_names}
	swapped_tts = {name: permute_tt(wire_normal[name], swap_perm) for name in all_names}

	# Check which inputs are symmetric
	print("\nInput symmetry:")
	for name in ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]:
		swapped = swapped_tts[name]
		# Find which wire matches
		for name2 in ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]:
			if normal_tts[name2] == swapped:
				print(f"  swap({name}) = {name2}")
				break

	# For each gate, find if its swapped version matches any existing gate
	print("\nGate swap-equivalences:")
	symmetric_gates = []  # gate whose tt is unchanged under swap
	matched_pairs = []     # (gi, gj) where swap(gi) == gj
	unmatched = []         # gates whose swapped tt doesn't match any gate

	gate_tt_to_name = {}
	for name in all_names:
		gate_tt_to_name[normal_tts[name]] = gate_tt_to_name.get(normal_tts[name], [])
		gate_tt_to_name[normal_tts[name]].append(name)

	for gname in gates:
		swapped = swapped_tts[gname]
		if swapped == normal_tts[gname]:
			symmetric_gates.append(gname)
		elif swapped in gate_tt_to_name:
			matches = gate_tt_to_name[swapped]
			matched_pairs.append((gname, matches))
		else:
			unmatched.append(gname)

	print(f"\n  Symmetric (unchanged under swap): {len(symmetric_gates)}")
	for g in symmetric_gates:
		print(f"    {g}: swap({g}) == {g}")

	print(f"\n  Matched pairs (swap(gi) == gj): {len(matched_pairs)}")
	seen_pairs = set()
	pair_count = 0
	for gname, matches in matched_pairs:
		for m in matches:
			pair = tuple(sorted([gname, m]))
			if pair not in seen_pairs and pair[0] != pair[1]:
				seen_pairs.add(pair)
				pair_count += 1
				print(f"    swap({gname}) == {m}")

	print(f"\n  Unmatched (swapped tt not in circuit): {len(unmatched)}")
	for g in unmatched:
		print(f"    {g}")

	# Key metric: how many gates could be saved by exploiting symmetry?
	print(f"\n--- Symmetry savings potential ---")
	print(f"  Total gates: {len(gates)}")
	print(f"  Symmetric gates (self-dual under swap): {len(symmetric_gates)}")
	print(f"  Matched pairs: {pair_count}")
	print(f"  Unmatched: {len(unmatched)}")
	print(f"  Potential savings: up to {pair_count} gates (if we compute one per pair)")
	print(f"  But need to account for: routing overhead (muxing swapped inputs)")

	# Analyze output symmetry
	print(f"\n--- Output symmetry ---")
	outputs = ["g28", "g33", "g48", "g49", "g52", "g50", "g51", "g53", "g25"]
	for i, oname in enumerate(outputs):
		swapped = swapped_tts[oname]
		if swapped == normal_tts[oname]:
			print(f"  out[{i}] ({oname}): SYMMETRIC (same under swap)")
		else:
			# Check if it matches another output
			for j, oname2 in enumerate(outputs):
				if normal_tts[oname2] == swapped:
					print(f"  out[{i}] ({oname}): swap -> out[{j}] ({oname2})")
					break
			else:
				print(f"  out[{i}] ({oname}): swapped tt doesn't match any output")

	# Analyze the dependency cone structure
	print(f"\n--- Dependency cone per gate (inputs used) ---")
	deps = {}
	input_names = ["a3", "a2", "a1", "a0", "b3", "b2", "b1", "b0"]

	# Gate definitions with their input references
	gate_defs = [
		("g0", ["b2", "b1"]), ("g1", ["b2", "a2"]), ("g2", ["b2", "a2"]),
		("g3", ["b0", "g0"]), ("g4", ["a1", "b1"]), ("g5", ["a1", "a2"]),
		("g6", ["a1", "b1"]), ("g7", ["g5", "a0"]), ("g8", ["g3", "g7"]),
		("g9", ["g7", "g3"]), ("g10", ["a3", "b3"]), ("g11", ["g6", "g4"]),
		("g12", ["g8", "g4"]), ("g13", ["g3", "b0"]), ("g14", ["g5", "g7"]),
		("g15", ["g9", "g11"]), ("g16", ["g14", "g13"]), ("g17", ["g1", "g6"]),
		("g18", ["g16", "g15"]), ("g19", ["g2", "g12"]), ("g20", ["g9", "g18"]),
		("g21", ["g12", "g1"]), ("g22", ["g19", "g18"]), ("g23", ["g11", "g19"]),
		("g24", ["g12", "g4"]), ("g25", ["g21", "g22"]), ("g26", ["g23", "g20"]),
		("g27", ["g21", "g17"]), ("g28", ["g10", "g16"]), ("g29", ["g26", "g20"]),
		("g30", ["g10", "g9"]), ("g31", ["g24", "g17"]), ("g32", ["g1", "g24"]),
		("g33", ["g28", "g31"]), ("g34", ["g32", "g29"]), ("g35", ["g28", "g25"]),
		("g36", ["g26", "g33"]), ("g37", ["g27", "g28"]), ("g38", ["g28", "g34"]),
		("g39", ["g10", "g35"]), ("g40", ["g38", "g29"]), ("g41", ["g37", "g18"]),
		("g42", ["g39", "g40"]), ("g43", ["g22", "g41"]), ("g44", ["g42", "g43"]),
		("g45", ["g36", "g44"]), ("g46", ["g22", "g35"]), ("g47", ["g45", "g46"]),
		("g48", ["g37", "g30"]), ("g49", ["g38", "g47"]), ("g50", ["g36", "g44"]),
		("g51", ["g43", "g42"]), ("g52", ["g45", "g46"]), ("g53", ["g39", "g40"]),
	]

	for name in input_names:
		deps[name] = {name}

	for gname, inputs in gate_defs:
		d = set()
		for inp in inputs:
			d |= deps[inp]
		deps[gname] = d

	# Count how many gates use only a-inputs, only b-inputs, or both
	a_only = b_only = both = symmetric_dep = 0
	for gname in gates:
		d = deps[gname]
		has_a = bool(d & {"a3", "a2", "a1", "a0"})
		has_b = bool(d & {"b3", "b2", "b1", "b0"})
		a_inputs = d & {"a3", "a2", "a1", "a0"}
		b_inputs = {x.replace("b", "a") for x in d & {"b3", "b2", "b1", "b0"}}
		is_symmetric_dep = (a_inputs == b_inputs)  # uses same "slots" from both

		if has_a and has_b:
			both += 1
			if is_symmetric_dep:
				symmetric_dep += 1
		elif has_a:
			a_only += 1
		elif has_b:
			b_only += 1

	print(f"  A-only gates: {a_only}")
	print(f"  B-only gates: {b_only}")
	print(f"  Mixed (both A and B): {both}")
	print(f"  Mixed with symmetric deps (same slots): {symmetric_dep}")

	# Key question: can we build a symmetric circuit?
	# In a symmetric circuit, we'd compute a "canonical" half where a <= b (lexicographic),
	# then the other half is free by symmetry.
	# But we need a comparator circuit to determine if a <= b, which costs gates.
	print(f"\n--- Symmetric circuit feasibility ---")
	# Count unique (a,b) pairs where a != b
	unique_unordered = 0
	self_pairs = 0
	for a in range(16):
		for b in range(16):
			if a < b:
				unique_unordered += 1
			elif a == b:
				self_pairs += 1
	print(f"  Total input pairs: 256")
	print(f"  Self-pairs (a==b): {self_pairs}")
	print(f"  Unordered pairs (a<b): {unique_unordered}")
	print(f"  By symmetry, only need {self_pairs + unique_unordered} = {self_pairs + unique_unordered} unique computations")

	# What does this mean for circuit design?
	print(f"\n  Strategy: sort inputs so a <= b, compute multiply, unsort outputs")
	print(f"  Cost: 4-bit comparator + 4x 2:1 mux = ~12-16 gates overhead")
	print(f"  Savings: eliminate {pair_count} duplicated gates")
	print(f"  Net: {pair_count} - ~14 = ~{pair_count - 14} gates saved (if positive)")

	# Alternative: don't sort, but directly exploit functional symmetry
	print(f"\n  Alternative: use symmetric sub-expressions directly")
	print(f"  e.g., (a1 & b1) is already symmetric")
	print(f"  e.g., (a2 | b2) + (b2 | a2) = same, no duplication needed")
	print(f"  But (a1 | a2) and (b1 | b2) are swap-equivalents that both exist")

	# Find specific swap-equivalent pairs that are both in the circuit
	print(f"\n--- Specific duplicated computations ---")
	for gname, matches in matched_pairs:
		for m in matches:
			if m in gates and gname in gates and gname < m:
				# Show what each computes
				g_deps = deps[gname]
				m_deps = deps[m]
				print(f"  {gname} (deps: {sorted(g_deps)}) <-> {m} (deps: {sorted(m_deps)})")


if __name__ == "__main__":
	main()
