"""How data is wrapped by each layer at the sender and unwrapped at the receiver."""
import sys
LAYERS = [("Application", "HTTP"), ("Transport", "TCP"), ("Network", "IP"),
          ("Data link", "ETH")]

def send(message):
    pdu = message
    for layer, tag in LAYERS:
        # TODO 1 (completed): wrap pdu with this layer's header "[tag|" and, for the
        # data link layer only, also a trailer "|FCS]"; other layers close with "]"
        head = "[" + tag + "│"
        tail = "│FCS]" if tag == "ETH" else "]"
        pdu = head + pdu + tail
        print(f"{layer:<13}adds {tag:<4} -> {len(pdu):3d} bytes")
    return pdu

def receive(frame):
    pdu = frame
    for layer, tag in reversed(LAYERS):
        head = "[" + tag + "│"
        tail = "│FCS]" if tag == "ETH" else "]"
        assert pdu.startswith(head) and pdu.endswith(tail), f"{layer}: bad header"
        pdu = pdu[len(head):-len(tail)]
    return pdu

msg = "GET /results" if len(sys.argv) < 2 else "x" * int(sys.argv[1])
frame = send(msg)
shown = frame if len(frame) < 80 else frame[:30] + "..." + frame[-30:]
print("on the wire:", shown)
print("delivered  :", receive(frame) if len(msg) < 40 else f"{len(receive(frame))} bytes (OK)")
print(f"overhead   : {len(frame) - len(msg)} bytes for {len(msg)} bytes of data "
      f"({(len(frame) - len(msg)) / len(frame):.1%} of the frame)")
