"""Link utilisation of stop-and-wait and sliding-window protocols on different links."""
import math

def utilisation(frame_bits, rate_bps, distance_m, window, speed=2e8):
    tx = frame_bits / rate_bps                  # transmission time
    prop = distance_m / speed                   # propagation time
    # TODO 1 (completed): a = prop / tx ; utilisation = window / (1 + 2a), at most 1
    a = prop / tx
    u = min(1.0, window / (1 + 2 * a))
    return u, a

links = [("Campus LAN, 200 m, 1 Gbps", 1e9, 200),
         ("City fibre, 50 km, 1 Gbps", 1e9, 50_000),
         ("Satellite, 36,000 km, 10 Mbps", 10e6, 36_000_000)]
for name, rate, dist in links:
    u1, a = utilisation(12_000, rate, dist, 1)
    u7, _ = utilisation(12_000, rate, dist, 7)
    u127, _ = utilisation(12_000, rate, dist, 127)
    print(f"{name:<31} a = {a:7.2f}  stop-and-wait {u1:6.1%}  "
          f"W=7 {u7:6.1%}  W=127 {u127:6.1%}")

print("\n--- head-office link: 400 km, 1 Gbps, 1,500-byte frames ---")
tx = 12_000 / 1e9; prop = 400_000 / 2e8; a = prop / tx
print(f"transmission time {tx*1e6:.1f} us, propagation time {prop*1e3:.2f} ms, a = {a:.2f}")
print(f"stop-and-wait utilisation {1/(1+2*a):.4%} -> {1/(1+2*a)*1000:.2f} Mbps")
W = math.ceil(1 + 2 * a)
print(f"smallest window for 100% use: 1 + 2a = {1+2*a:.2f} -> W = {W}")
print("Go-Back-N bits:", math.ceil(math.log2(W + 1)), "| Selective Repeat bits:", math.ceil(math.log2(2 * W)))
print(f"Selective Repeat W=64: utilisation {64/(1+2*a):.2%}, throughput {64/(1+2*a)*1000:.1f} Mbps, receiver buffer {64*1500:,} bytes")
print(f"Full window receiver buffer {W*1500:,} bytes")
_, a_sat = utilisation(12_000, 10e6, 36_000_000, 1)
print(f"satellite: a = {a_sat:.0f} -> smallest window for 100% = {math.ceil(1 + 2*a_sat)}")
