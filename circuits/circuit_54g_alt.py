"""
FP4 Multiplier - 54-gate circuit (diverse SA run 700)
"""

def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
	# 54 gates (SA-diverse-700)
	g0 = b3 ^ a3
	g1 = b1 ^ a1
	g2 = b1 | b2
	g3 = b0 ^ g2
	g4 = g3 | g2
	g5 = a1 | a2
	g6 = a0 ^ g5
	g7 = a0 | g6
	g8 = b1 & a1
	g9 = g6 | g3
	g10 = a2 | b2
	g11 = a2 & b2
	g12 = g7 & g4
	g13 = g6 & g3
	g14 = g13 & g1
	g15 = g12 ^ g14
	g16 = g15 ^ g13
	g17 = g11 ^ g8
	g18 = g17 ^ g9
	g19 = g0 & g12
	g20 = g18 ^ g10
	g21 = g1 ^ g20
	g22 = g8 | g21
	g23 = g22 & g18
	g24 = g21 & g16
	g25 = g15 & g20
	g26 = g25 & g18
	g27 = g24 & g8
	g28 = g16 ^ g24
	g29 = g26 ^ g19
	g30 = g23 & g11
	g31 = g29 ^ g25
	g32 = g23 | g11
	g33 = g30 ^ g19
	g34 = g15 ^ g33
	g35 = g28 & g32
	g36 = g11 & g27
	g37 = g19 & g29
	g38 = g34 ^ g25
	g39 = g36 ^ g19
	g40 = g35 ^ g19
	g41 = g28 ^ g40
	g42 = g41 ^ g37
	g43 = g37 & g41
	g44 = g38 & g43
	g45 = g13 & g37
	g46 = g45 | g33
	g47 = g39 ^ g24
	g48 = g43 ^ g38
	g49 = g47 & g44
	g50 = g44 ^ g47
	g51 = g49 & g31
	g52 = g49 ^ g31
	g53 = g40 ^ g51
	return [g19, g39, g46, g53, g52, g50, g48, g42, g26]


if __name__ == "__main__":
	from fp4_multiplier import verify_circuit
	success, failures = verify_circuit(write_your_multiplier_here)
	print(f"Verification: {256-len(failures)}/256 correct")
