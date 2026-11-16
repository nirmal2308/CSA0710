"""Longest-prefix match on the main-campus routing table (Q3)."""
import ipaddress
TABLE = [("10.0.0.0/8", "192.0.2.1"), ("10.1.0.0/16", "192.0.2.5"),
         ("10.1.2.0/24", "192.0.2.9"), ("10.1.2.128/25", "192.0.2.13"),
         ("0.0.0.0/0", "198.51.100.1")]
for dst in ("10.1.2.200", "10.1.2.100", "10.1.9.9", "10.7.7.7", "8.8.8.8"):
    ip = ipaddress.ip_address(dst)
    matches = [(ipaddress.ip_network(n), nh) for n, nh in TABLE if ip in ipaddress.ip_network(n)]
    best = max(matches, key=lambda m: m[0].prefixlen)
    print(f"{dst:<11} matches {[str(m[0]) for m in matches]} -> longest /{best[0].prefixlen} {best[0]} via {best[1]}")
