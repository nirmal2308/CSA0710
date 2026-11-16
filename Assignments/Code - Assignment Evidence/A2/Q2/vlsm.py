"""Variable-length subnetting (VLSM) of 192.168.10.0/24 for a college campus."""
import math
import ipaddress

def to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d

def to_ip(n):
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))

def vlsm(base, needs, quiet=False):
    addr = to_int(base)
    plan = []
    for name, hosts in sorted(needs, key=lambda x: -x[1]):
        # TODO 1 (completed): smallest power-of-two block holding hosts + 2 addresses
        block = 1 << math.ceil(math.log2(hosts + 2))
        prefix = 32 - int(math.log2(block))
        net = addr
        first, last, bcast = net + 1, net + block - 2, net + block - 1
        if not quiet:
            print(f"{name:<12}{to_ip(net)}/{prefix}  hosts {to_ip(first)} - {to_ip(last)}  bcast {to_ip(bcast)}")
        plan.append((name, to_ip(net), prefix))
        addr = net + block                      # move to the next block
    return to_ip(addr), plan

if __name__ == "__main__":
    needs = [("Labs", 100), ("Staff", 50), ("Library", 25), ("WAN link", 2)]
    nxt, plan = vlsm("192.168.10.0", needs)
    print("next free address:", nxt)

    # ---- verification with the ipaddress module ----
    print("\n--- verification with ipaddress ---")
    nets = [ipaddress.ip_network(f"{n}/{p}") for _, n, p in plan]
    for (name, _, _), net in zip(plan, nets):
        print(f"{name:<9} {str(net):<18} mask {net.netmask}  usable {net.num_addresses - 2:>3}  "
              f"first {net[1]}  last {net[-2]}  broadcast {net.broadcast_address}")
    overlap = any(a.overlaps(b) for i, a in enumerate(nets) for b in nets[i + 1:])
    print("any overlap between subnets:", overlap)
    parent = ipaddress.ip_network("192.168.10.0/24")
    print("all inside 192.168.10.0/24 :", all(n.subnet_of(parent) for n in nets))
    free = int(ipaddress.ip_address(parent.broadcast_address)) - to_int(nxt) + 1
    print("addresses still free        :", free)

    # ---- the hostel trap: add 60 hosts ----
    print("\n--- hostel network (60 hosts) ---")
    need_block = 1 << math.ceil(math.log2(60 + 2))
    print(f"60 hosts + 2 -> block of {need_block} (/{32 - int(math.log2(need_block))}); free addresses left in the /24: {free}")
    start = to_int(nxt)
    aligned = (start + need_block - 1) // need_block * need_block
    print(f"next /26 boundary after {nxt} is {to_ip(aligned)} -> "
          f"{'INSIDE' if aligned + need_block - 1 <= to_int('192.168.10.255') else 'OUTSIDE'} the /24")
    fix = ipaddress.ip_network("192.168.11.0/26")
    print("smallest change: give the hostel", fix, "(usable", fix.num_addresses - 2, ") from 192.168.11.0/24;",
          "campus summary becomes", ipaddress.ip_network("192.168.10.0/23"))

    # ---- alternative: smallest-first ----
    print("\n--- alternative: smallest subnet first ---")
    addr = to_int("192.168.10.0")
    print("naive (no alignment):")
    for name, hosts in sorted(needs, key=lambda x: x[1]):
        block = 1 << math.ceil(math.log2(hosts + 2))
        prefix = 32 - int(math.log2(block))
        true_net = ipaddress.ip_network(f"{to_ip(addr)}/{prefix}", strict=False)
        flag = "" if int(true_net.network_address) == addr else f"  <-- misaligned: /{prefix} containing it starts at {true_net.network_address}"
        print(f"  {name:<9} start {to_ip(addr):<15} size {block:>3}{flag}")
        addr += block
    print("aligned smallest-first:")
    addr = to_int("192.168.10.0")
    used = []
    for name, hosts in sorted(needs, key=lambda x: x[1]):
        block = 1 << math.ceil(math.log2(hosts + 2))
        aligned = (addr + block - 1) // block * block
        gap = aligned - addr
        print(f"  {name:<9} {to_ip(aligned)}/{32 - int(math.log2(block))}  (wasted gap before it: {gap})")
        used.append(gap)
        addr = aligned + block
    print("  total wasted in gaps:", sum(used), "| next free:", to_ip(addr))

    # ---- summarisation ----
    print("\n--- route summarisation ---")
    camp = [ipaddress.ip_network(f"172.16.{i}.0/24") for i in (8, 9, 10, 11)]
    print("collapse 172.16.8-11.0/24 ->", list(ipaddress.collapse_addresses(camp)))
    s21 = ipaddress.ip_network("172.16.8.0/21")
    print("172.16.8.0/21 covers", s21[0], "-", s21[-1], "=", s21.num_addresses // 256, "x /24 networks, but only 5 exist")
    print("not owned but attracted:", [str(ipaddress.ip_network(f"172.16.{i}.0/24")) for i in (13, 14, 15)])
