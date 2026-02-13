"""
FP4 Multiplier - 58-gate circuit (diverse SA run 307)
"""

def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
	# 58 gates (SA-diverse-307)
	g0 = b3 ^ a3
	g1 = b1 & a1
	g2 = b1 | b2
	g3 = b2 | a2
	g4 = a2 | a1
	g5 = b0 ^ g2
	g6 = 1 - g3
	g7 = g4 ^ a0
	g8 = b0 & a0
	g9 = b2 & a2
	g10 = g7 | g4
	g11 = g8 & g1
	g12 = b0 | g5
	g13 = g1 ^ g9
	g14 = g7 | g5
	g15 = g7 & g5
	g16 = b1 ^ a1
	g17 = g6 & g8
	g18 = g12 & g10
	g19 = g9 & g11
	g20 = g18 & g0
	g21 = g17 ^ g15
	g22 = g14 ^ g16
	g23 = 1 - g17
	g24 = g14 ^ g13
	g25 = g3 ^ g24
	g26 = g22 & g15
	g27 = g16 ^ g25
	g28 = g11 ^ g9
	g29 = g20 & g23
	g30 = g9 & g22
	g31 = g30 & g24
	g32 = g19 ^ g20
	g33 = g18 ^ g26
	g34 = g33 & g27
	g35 = g32 ^ g34
	g36 = g31 ^ g20
	g37 = g31 & g26
	g38 = g34 | g26
	g39 = g21 ^ g33
	g40 = g28 | g38
	g41 = g25 & g39
	g42 = g41 ^ g20
	g43 = g40 & g29
	g44 = g39 ^ g42
	g45 = g37 | g36
	g46 = g44 ^ g31
	g47 = g46 & g43
	g48 = g47 & g35
	g49 = g35 ^ g47
	g50 = g42 & g48
	g51 = g42 ^ g48
	g52 = g43 ^ g46
	g53 = g40 ^ g20
	g54 = g53 ^ g38
	g55 = g50 ^ g54
	g56 = g18 ^ g53
	g57 = g29 ^ g56
	return [g20, g32, g45, g55, g51, g49, g52, g57, g17]


if __name__ == "__main__":
	from fp4_multiplier import verify_circuit
	success, failures = verify_circuit(write_your_multiplier_here)
	print(f"Verification: {256-len(failures)}/256 correct")
