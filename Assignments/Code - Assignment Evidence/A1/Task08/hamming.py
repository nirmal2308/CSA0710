"""Hamming(7,4) code: correct a single-bit error in a 4-bit sensor reading."""

def encode(d):                     # d = [d1, d2, d3, d4]
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]      # positions 1..7

def decode(c):
    # TODO 1 (completed): syndrome bits, error position, correction
    c = c[:]
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]          # positions 1,3,5,7
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]          # positions 2,3,6,7
    s3 = c[3] ^ c[4] ^ c[5] ^ c[6]          # positions 4,5,6,7
    pos = s1 + 2 * s2 + 4 * s3
    if pos:
        c[pos - 1] ^= 1
    return pos, [c[2], c[4], c[5], c[6]]

word = encode([1, 0, 1, 1])
print("codeword       :", "".join(map(str, word)))
for flip in (None, 5):
    rx = word[:]
    if flip:
        rx[flip - 1] ^= 1
    pos, data = decode(rx)
    print(f"error at {str(flip):<4}: syndrome {pos}, data {''.join(map(str, data))}")

print("\n--- two-bit error: the decoder 'corrects' the wrong bit ---")
for a, b in ((2, 5), (1, 4), (3, 6)):
    rx = word[:]
    rx[a - 1] ^= 1
    rx[b - 1] ^= 1
    pos, data = decode(rx)
    print(f"flip positions {a} and {b}: received {''.join(map(str, rx))}  syndrome {pos}  "
          f"decoded data {''.join(map(str, data))}  (sent 1011)  -> {'WRONG' if data != [1,0,1,1] else 'ok'}")
print("\nworked example from the task: received 0110111")
rx = [0, 1, 1, 0, 1, 1, 1]
pos, data = decode(rx)
print("syndrome (error position):", pos, " corrected data:", "".join(map(str, data)))

ber, t_retx = 1e-3, 40.0
n_fec = 21                                   # 16 data + 5 Hamming check bits
p_fec_bad = 1 - (1 - ber) ** n_fec - n_fec * ber * (1 - ber) ** (n_fec - 1)
n_arq = 16 + 8                               # 16 data + 8-bit CRC for detection
p_arq = 1 - (1 - ber) ** n_arq
attempts = 1 / (1 - p_arq)
print(f"\nFEC : {n_fec} bits/reading, residual (2+ bit) error probability {p_fec_bad:.2e}, "
      f"extra delay 0 ms (no waiting)")
print(f"ARQ : {n_arq} bits/attempt, P(retransmit) = {p_arq:.4f}, attempts/reading {attempts:.4f}, "
      f"bits/reading {n_arq * attempts:.2f}, average extra delay {p_arq / (1 - p_arq) * t_retx:.3f} ms")
