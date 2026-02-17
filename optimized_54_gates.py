"""
FP4 Multiplier - 54-gate circuit (diverse SA run 703)
"""

def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
	# 54 gates (SA-diverse-703)
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


if __name__ == "__main__":
	from fp4_multiplier import verify_circuit
	success, failures = verify_circuit(write_your_multiplier_here)
	print(f"Verification: {256-len(failures)}/256 correct")
