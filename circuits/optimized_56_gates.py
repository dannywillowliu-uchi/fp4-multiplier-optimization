"""
FP4 Multiplier - 56-gate circuit (diverse SA run 606)
"""

def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
	# 56 gates (SA-diverse-606)
	g0 = a1 ^ b1
	g1 = a1 | b1
	g2 = a2 | b2
	g3 = b2 & a2
	g4 = b2 | b1
	g5 = b2 ^ a2
	g6 = b0 ^ g4
	g7 = b3 ^ a3
	g8 = a2 | a1
	g9 = g8 | a0
	g10 = g4 | g6
	g11 = 1 - g2
	g12 = g9 & g10
	g13 = g8 ^ a0
	g14 = g6 | g13
	g15 = g0 | g14
	g16 = g7 & g12
	g17 = g3 & g1
	g18 = g13 & g6
	g19 = g7 & g18
	g20 = g18 & g0
	g21 = g1 ^ g14
	g22 = g12 ^ g20
	g23 = 1 - g15
	g24 = g21 ^ g5
	g25 = g18 ^ g22
	g26 = g24 ^ g0
	g27 = g24 & g25
	g28 = g25 ^ g27
	g29 = g3 | g23
	g30 = 1 - g26
	g31 = g17 & g30
	g32 = g26 & g22
	g33 = g28 & g29
	g34 = g11 & g32
	g35 = g31 ^ g16
	g36 = g16 ^ g33
	g37 = g35 ^ g22
	g38 = g36 ^ g28
	g39 = g37 ^ g32
	g40 = g17 & g23
	g41 = g19 | g35
	g42 = g16 ^ g40
	g43 = g16 ^ g34
	g44 = g16 & g43
	g45 = g44 & g38
	g46 = g32 ^ g43
	g47 = g45 & g39
	g48 = g27 ^ g42
	g49 = g47 ^ g48
	g50 = g48 & g47
	g51 = g37 & g50
	g52 = g44 ^ g38
	g53 = g39 ^ g45
	g54 = g50 ^ g46
	g55 = g51 ^ g36
	return [g16, g42, g41, g55, g54, g49, g53, g52, g34]


if __name__ == "__main__":
	from fp4_multiplier import verify_circuit
	success, failures = verify_circuit(write_your_multiplier_here)
	print(f"Verification: {256-len(failures)}/256 correct")
