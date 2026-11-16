"""CRC error detection for frames sent between two switches."""
from itertools import combinations

def mod2_div(dividend, divisor):
    """Return the remainder of modulo-2 (XOR) division of two bit strings."""
    rem = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        # TODO 1 (completed): if the leading bit is 1, XOR the divisor in at position i
        if rem[i] == "1":
            for j in range(len(divisor)):
                rem[i + j] = "0" if rem[i + j] == divisor[j] else "1"
    return "".join(rem[-(len(divisor) - 1):])

def encode(data, gen):
    crc = mod2_div(data + "0" * (len(gen) - 1), gen)
    return data + crc

def check(frame, gen):
    return set(mod2_div(frame, gen)) == {"0"}

GEN = "1011"                                   # x^3 + x + 1
frame = encode("1101011011", GEN)
print("transmitted:", frame)
print("no error   :", check(frame, GEN))
bad = frame[:4] + ("1" if frame[4] == "0" else "0") + frame[5:]
print("1-bit error:", check(bad, GEN))
burst = frame[:2] + "".join("1" if b == "0" else "0" for b in frame[2:5]) + frame[5:]
print("3-bit burst:", check(burst, GEN))

# ---------------- extra work asked in Task 7 ----------------
print("\n--- extra work ---")
print("CRC bits for 1101011011 :", mod2_div("1101011011000", GEN))
print("received 1101011011101 remainder:", mod2_div("1101011011101", GEN),
      "-> accepted" if check("1101011011101", GEN) else "-> REJECTED")

def flip(frame, positions):
    f = list(frame)
    for p in positions:
        f[p] = "1" if f[p] == "0" else "0"
    return "".join(f)

n = len(frame)
undetected = []
for k in range(1, 5):
    for pos in combinations(range(n), k):
        if check(flip(frame, pos), GEN):
            undetected.append(pos)
print("undetected patterns with <= 4 flipped bits in a 13-bit frame:", len(undetected))
for pos in undetected[:6]:
    pat = "".join("1" if i in pos else "0" for i in range(n))
    print("  error pattern", pat, "weight", len(pos), "-> accepted (undetected)")

def parity_ok(bits):            # even parity over the whole frame
    return bits.count("1") % 2 == 0
data = "1101011011"
pf = data + ("1" if data.count("1") % 2 else "0")
print("\neven-parity frame:", pf)
tests = {"2-bit adjacent": [0, 1], "2-bit, 7 apart": [0, 7],
         "4-bit pattern 11101 (x^4+x^3+x^2+1)": [2, 3, 4, 6], "4-bit burst 1111": [3, 4, 5, 6]}
for name, pos in tests.items():
    pat13 = "".join("1" if i in pos else "0" for i in range(13))
    crc_det = not check(flip(frame, pos), GEN)
    par_det = len(pos) % 2 == 1          # even parity detects exactly the odd-weight errors
    print(f"{name:<38} pattern {pat13}  CRC-3 {'detects' if crc_det else 'MISSES'}   parity {'detects' if par_det else 'MISSES'}")
m3 = [i for i in range(13) if "0000000001011"[i] == "1"]
print("3-bit pattern 0000000001011 (= generator): CRC",
      "detects" if not check(flip(frame, m3), GEN) else "MISSES",
      "| parity", "detects" if len(m3) % 2 == 1 else "MISSES")

block = ["1011", "0110", "1100", "0101"]
rp = [r.count("1") % 2 for r in block]
cp = [sum(int(block[r][c]) for r in range(4)) % 2 for c in range(4)]
print("\n2-D parity block:", block, "row parity", rp, "column parity", cp,
      "corner parity", sum(rp) % 2)

words = [0x4500, 0x0073, 0x0000, 0x4000]
s = sum(words)
while s >> 16:
    s = (s & 0xFFFF) + (s >> 16)
print(f"\nInternet checksum: sum = {sum(words):#06x}, ones-complement = {(~s) & 0xFFFF:#06x}")
