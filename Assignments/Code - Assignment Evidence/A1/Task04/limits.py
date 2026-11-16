"""Nyquist and Shannon limits for the transmission media proposed for a campus."""
import math

def nyquist(bandwidth_hz, levels):
    # TODO 1 (completed): Nyquist maximum bit rate for a noiseless channel
    return 2 * bandwidth_hz * math.log2(levels)

def shannon(bandwidth_hz, snr_db):
    # TODO 2 (completed): dB -> ratio, then Shannon capacity
    snr = 10 ** (snr_db / 10)
    return bandwidth_hz * math.log2(1 + snr)

media = [("Telephone line", 3_100, 30), ("Cat6 pair", 250e6, 40),
         ("Wi-Fi 6 channel", 160e6, 25)]
for name, bw, snr in media:
    print(f"{name:<16} Shannon limit {shannon(bw, snr) / 1e6:10.2f} Mbps")
print(f"Nyquist, 3,100 Hz with 4 levels: {nyquist(3_100, 4) / 1e3:.1f} kbps")

# ---- extra work asked in the task ----
print("\n--- extra calculations ---")
print(f"Cat6 250 MHz @ 40 dB : {shannon(250e6, 40) / 1e6:8.1f} Mbps")
print(f"Cat6 250 MHz @ 15 dB : {shannon(250e6, 15) / 1e6:8.1f} Mbps")
print(f"Wi-Fi 6 160 MHz @ 15 dB (welding area): {shannon(160e6, 15) / 1e6:8.1f} Mbps")
need = 56_000 / 3_100                       # bits per Hz required
snr_ratio = 2 ** need - 1
print(f"56 kbps over 3,100 Hz needs {need:.3f} bit/s/Hz -> SNR {snr_ratio:,.0f} "
      f"= {10 * math.log10(snr_ratio):.2f} dB")
