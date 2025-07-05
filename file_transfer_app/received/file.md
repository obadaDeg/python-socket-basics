# 🛡️ Python Socket Module - Cybersecurity Notes

## 📚 Overview

The `socket` module in Python provides low-level networking interfaces for handling raw communication, vital in cybersecurity for tasks like scanning, sniffing, enumeration, and crafting connections.

---

## 🔌 Socket Families

Socket families define the addressing structure and type of communication. Each is tailored for specific system architectures or networking tasks.

### ✅ Common Socket Families & Their Formats

| Family         | Description | Format |
|----------------|-------------|--------|
| **AF_UNIX**    | Unix domain sockets (local IPC) | `file path` or abstract namespace (starts with `\0`) |
| **AF_INET**    | IPv4 networking | `(host, port)` — e.g. `('127.0.0.1', 8080)` <br> Special: `''` (bind all), `'<broadcast>'` (broadcast) |
| **AF_INET6**   | IPv6 networking | `(host, port, flowinfo, scope_id)` |
| **AF_NETLINK** | Linux-only kernel <-> user space communication | `(pid, groups)` |
| **AF_TIPC**    | Clustered systems (Linux-only) | `(addr_type, v1, v2, v3 [, scope])` |
| **AF_CAN**     | Controller Area Network (cars, drones) | `('can0',)` <br> Extended: `ISOTP`, `J1939`, etc. |
| **PF_SYSTEM**  | macOS-specific system sockets | `("control_name")` or `(id, unit)` |
| **AF_BLUETOOTH** | Bluetooth sockets | `L2CAP`: `(bdaddr, psm)`<br>`RFCOMM`: `(bdaddr, channel)`<br>`HCI`: `(device_id,)` or `bdaddr`<br>`SCO`: `bdaddr` |
| **AF_ALG**     | Linux Kernel crypto interface | `(type, name [, feat, mask])` <br> Example: `('hash', 'sha256')` |
| **AF_VSOCK**   | VM ↔ Host (used in virtualization) | `(CID, port)` |
| **AF_PACKET**  | Raw link-layer access (Linux) | `(ifname, proto[, pkttype[, hatype[, addr]]])` |
| **AF_QIPCRTR** | Qualcomm IPC router (Linux-only) | `(node, port)` |
| **AF_HYPERV**  | Windows Hyper-V guest ↔ host | `(vm_id, service_id)` (both UUIDs) |

---

## 📡 Protocols

| Protocol           | Description |
|--------------------|-------------|
| **IPPROTO_UDPLITE** | Variant of UDP with adjustable checksum coverage (Linux, FreeBSD) |

---

## ⚠️ Important Notes

- ❗ **DNS Resolution**: Use IPs instead of hostnames for deterministic behavior.
- ⚙️ **Blocking Modes**: Use `setblocking(False)` or `settimeout(seconds)` for non-blocking or timeout control.
- 🧯 **Error Handling**: All socket operations may raise `OSError`. Always use try-except blocks.
  
```python
import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 80))
except OSError as e:
    print(f"Error: {e}")
```

## 🛠️ Useful Functions
| Function | Purpose |
|`socket()` |	Create a new socket |
| `bind()` | 	Bind socket to an address |
| `connect()` |	Connect to remote socket |
| `listen()` |	Start listening for incoming connections |
| `accept()` |	Accept an incoming connection | 
| `recv()` / `send()` | Receive/send data | 
| `setblocking()` | Set blocking/non-blocking mode |
| `settimeout()` | Set a timeout for operations |

## 🧠 Cybersecurity Use Cases
- Port Scanning (connect_ex)

- Banner Grabbing

- Proxy and Tunneling Tools

- Packet Sniffing with AF_PACKET

- Socket-based Backdoors

- Bluetooth-based Attacks (AF_BLUETOOTH)

- IPC Abuse (AF_UNIX)


# 🧾 References
- Python Docs: https://docs.python.org/3/library/socket.html

- RFC 3493: Basic Socket Interface Extensions for IPv6

- Linux man 7 socket