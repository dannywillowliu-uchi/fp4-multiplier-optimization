"""
FP4 Multiplier - 57 gates
From peephole on 58-gate: window [34,38,40,43,53,54,56] 7->6
"""

def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
	# 57 gates (peephole-from-58)
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
	g34 = g31 ^ g20
	g35 = g31 & g26
	g36 = g21 ^ g33
	g37 = g25 & g36
	g38 = g37 ^ g20
	g39 = g36 ^ g38
	g40 = g35 | g34
	g41 = g39 ^ g31
	g42 = g27 & g33
	g43 = g32 ^ g42
	g44 = g33 ^ g42
	g45 = g44 & g28
	g46 = g20 ^ g45
	g47 = g44 ^ g46
	g48 = g29 ^ g47
	g49 = g47 & g29
	g50 = g41 & g49
	g51 = g50 & g43
	g52 = g43 ^ g50
	g53 = g38 & g51
	g54 = g38 ^ g51
	g55 = g49 ^ g41
	g56 = g53 ^ g46
	return [g20, g32, g40, g56, g54, g52, g55, g48, g17]


if __name__ == "__main__":
	from fp4_multiplier import verify_circuit
	success, failures = verify_circuit(write_your_multiplier_here)
	print(f"Verification: {256-len(failures)}/256 correct")
