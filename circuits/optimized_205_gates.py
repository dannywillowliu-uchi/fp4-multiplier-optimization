"""
FP4 Multiplier - Optimized Solution

Gate count: 205 gates (AND: 85, OR: 59, NOT: 61)
Optimization: NOT-of-NOT pattern elimination applied
Encoding: Optimized permutation [1, 7, 3, 4, 0, 2, 6, 5]

Reduced from 242 gates by eliminating 37 redundant NOT-of-NOT patterns.
"""


# INPUT_REMAP: Maps new input codes to original FP4 codes
INPUT_REMAP = {
    0: 1, 1: 7, 2: 3, 3: 4, 4: 0, 5: 2, 6: 6, 7: 5,
    8: 9, 9: 15, 10: 11, 11: 12, 12: 0, 13: 10, 14: 14, 15: 13
}


def write_your_multiplier_here(a3, a2, a1, a0, b3, b2, b1, b0):
	# 205 gates
	g0 = a2 | a0
	g1 = 1 - g0
	g2 = b2 | b0
	g3 = 1 - g2
	g4 = g1 & g3
	g5 = 1 - b0
	g6 = a0 & g5
	g7 = 1 - a0
	g8 = g7 & b0
	g9 = g6 | g8
	g10 = 1 - g9
	g11 = a2 & g3
	g12 = b2 & g1
	g13 = g11 | g12
	g14 = 1 - g13
	g15 = g10 | g14
	g16 = 1 - g15
	g17 = a1 & b1
	g18 = a1 | b1
	g19 = 1 - g18
	g20 = g17 | g19
	g21 = 1 - g20
	g22 = a3 | b3
	g23 = 1 - g22
	g24 = a3 & b3
	g25 = g23 | g24
	g26 = 1 - g25
	g27 = g21 | g26
	g28 = 1 - g27
	g29 = g21 & g26
	g30 = g28 | g29
	g31 = 1 - g30
	g32 = g4 & g31
	g33 = g16 | g32
	g34 = a0 & b0
	g35 = a2 & b2
	g36 = g34 & g35
	g37 = g16 & g31
	g38 = a2 | b2
	g39 = 1 - g38
	g40 = g7 & g26
	g41 = 1 - g40
	g42 = g10 & g41
	g43 = 1 - g42
	g44 = g39 & g43
	g45 = g36 | g37
	g46 = g44 | g45
	g47 = a1 & g7
	g48 = g11 & g47
	g49 = b0 | g26
	g50 = 1 - g49
	g51 = b2 | g50
	g52 = 1 - g51
	g53 = b0 & g20
	g54 = g26 & g53
	g55 = g52 | g54
	g56 = a2 & g55
	g57 = a2 & g25
	g58 = g3 | g57
	g59 = g21 & g49
	g60 = g58 & g59
	g61 = g56 | g60
	g62 = a0 & g61
	g63 = 1 - g47
	g64 = g10 & g63
	g65 = 1 - g64
	g66 = g28 & g65
	g67 = 1 - a1
	g68 = g67 & b0
	g69 = g17 | g68
	g70 = 1 - g69
	g71 = g40 & g70
	g72 = g66 | g71
	g73 = 1 - g72
	g74 = b2 | g73
	g75 = a0 | g26
	g76 = 1 - g75
	g77 = b2 & b0
	g78 = g7 & b1
	g79 = g68 & g78
	g80 = g77 | g79
	g81 = 1 - g80
	g82 = g76 | g81
	g83 = 1 - g82
	g84 = b2 & g5
	g85 = g78 & g84
	g86 = g83 | g85
	g87 = 1 - g86
	g88 = g74 & g87
	g89 = a2 | g88
	g90 = 1 - g89
	g91 = g48 | g62
	g92 = g90 | g91
	g93 = b1 | b0
	g94 = 1 - g93
	g95 = g12 & g93
	g96 = 1 - b1
	g97 = g96 & b0
	g98 = a0 & g38
	g99 = g84 | g97
	g100 = 1 - g99
	g101 = g98 & g100
	g102 = g95 | g101
	g103 = 1 - g102
	g104 = a1 | g103
	g105 = a1 & g97
	g106 = 1 - g105
	g107 = b2 & g106
	g108 = a2 | g107
	g109 = 1 - g108
	g110 = 1 - b2
	g111 = a1 & g110
	g112 = g77 | g111
	g113 = a2 & g112
	g114 = b1 | g8
	g115 = 1 - g114
	g116 = g113 & g115
	g117 = g109 | g116
	g118 = 1 - g117
	g119 = g104 & g118
	g120 = 1 - g119
	g121 = g26 & g120
	g122 = a1 & g8
	g123 = a1 & g26
	g124 = 1 - g123
	g125 = b0 & g124
	g126 = a0 & b1
	g127 = 1 - g125
	g128 = g127 & g126
	g129 = g122 | g128
	g130 = g35 & g129
	g131 = g13 & g17
	g132 = g21 & g38
	g133 = 1 - g35
	g134 = g34 & g133
	g135 = 1 - g132
	g136 = g135 & g134
	g137 = g131 | g136
	g138 = 1 - g137
	g139 = g26 | g138
	g140 = 1 - g139
	g141 = g121 | g140
	g142 = g130 | g141
	g143 = g67 & a0
	g144 = g39 & g143
	g145 = a2 & g67
	g146 = 1 - g145
	g147 = b2 & g146
	g148 = g6 | g113
	g149 = g147 & g148
	g150 = g144 | g149
	g151 = b1 & g150
	g152 = a2 & g7
	g153 = a2 | b1
	g154 = 1 - g153
	g155 = g152 | g154
	g156 = b0 & g111
	g157 = g155 & g156
	g158 = g151 | g157
	g159 = 1 - g158
	g160 = g26 | g159
	g161 = 1 - g160
	g162 = b2 & g94
	g163 = b1 & g143
	g164 = g105 | g163
	g165 = 1 - g164
	g166 = g39 & g164
	g167 = g17 & g35
	g168 = 1 - g162
	g169 = g26 & g168
	g170 = g67 & g152
	g171 = 1 - g170
	g172 = g169 & g171
	g173 = g162 | g167
	g174 = 1 - g173
	g175 = 1 - g166
	g176 = g175 & g174
	g177 = g172 & g176
	g178 = g161 | g177
	g179 = 1 - g84
	g180 = a1 & g179
	g181 = a0 | g180
	g182 = 1 - g181
	g183 = g97 & g111
	g184 = g182 | g183
	g185 = a2 & g184
	g186 = g17 & g185
	g187 = g147 & g163
	g188 = g162 | g187
	g189 = 1 - g188
	g190 = 1 - g185
	g191 = g190 & g189
	g192 = g26 | g165
	g193 = 1 - g192
	g194 = 1 - g191
	g195 = g194 & g193
	g196 = g26 & g191
	g197 = g186 | g195
	g198 = g196 | g197
	g199 = g97 & g144
	g200 = 1 - g169
	g201 = g200 & g199
	g202 = 1 - g199
	g203 = g172 & g202
	g204 = g201 | g203
	return [g172, g204, g198, g178, g142, g92, g46, g33, g4]


def verify_solution():
    """Verify the solution against all 256 input combinations."""
    # Original FP4 values
    FP4_VALUES = {
        0: 0.0, 1: 0.5, 2: 1.0, 3: 1.5, 4: 2.0, 5: 3.0, 6: 4.0, 7: 6.0,
        8: 0.0, 9: -0.5, 10: -1.0, 11: -1.5, 12: -2.0, 13: -3.0, 14: -4.0, 15: -6.0,
    }

    # New encoding
    MAGNITUDES = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
    perm = [1, 7, 3, 4, 0, 2, 6, 5]
    NEW_ENC = {}
    for new_mag, old_mag in enumerate(perm):
        NEW_ENC[new_mag] = MAGNITUDES[old_mag]
        NEW_ENC[new_mag + 8] = -MAGNITUDES[old_mag] if old_mag != 0 else 0.0

    def to_twos_complement(value, bits=9):
        if value < 0:
            return (1 << bits) + value
        return value

    # Build inverse remap
    inverse_remap = {}
    for orig_code in range(16):
        orig_val = FP4_VALUES[orig_code]
        for new_code in range(16):
            if NEW_ENC[new_code] == orig_val:
                if orig_code not in inverse_remap:
                    inverse_remap[orig_code] = new_code
                elif (new_code >= 8) == (orig_code >= 8):
                    inverse_remap[orig_code] = new_code

    errors = 0
    for a_orig in range(16):
        for b_orig in range(16):
            a_val = FP4_VALUES[a_orig]
            b_val = FP4_VALUES[b_orig]
            expected = int(a_val * b_val * 4)
            expected_tc = to_twos_complement(expected)

            a_mapped = inverse_remap[a_orig]
            b_mapped = inverse_remap[b_orig]

            a_bits = [(a_mapped >> (3 - i)) & 1 for i in range(4)]
            b_bits = [(b_mapped >> (3 - i)) & 1 for i in range(4)]

            output = write_your_multiplier_here(*a_bits, *b_bits)

            actual_tc = 0
            for bit in output:
                actual_tc = (actual_tc << 1) | int(bit)

            if actual_tc != expected_tc:
                errors += 1

    print(f"Verification: {256 - errors}/256 correct")
    return errors == 0


if __name__ == "__main__":
    print("FP4 Multiplier - Optimized 205-Gate Solution")
    print("=" * 60)
    print(f"Gate count: 205 (AND: 85, OR: 59, NOT: 61)")
    print(f"Encoding permutation: [1, 7, 3, 4, 0, 2, 6, 5]")
    print()
    verify_solution()
