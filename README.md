# PortScanner

Multi-threaded TCP port scanner written in Python. It resolves a target host, scans the chosen port range with a configurable number of threads, and reports the open ports with their common service names.

> Academic project from my Cybersecurity degree at FIAP (2021, *Development and Coding for Security*). It was my first security tool, kept here to show where I started.

## How it works

1. Prompts for the target (hostname or IP), the port range and the number of threads
2. Resolves the hostname with `socket.gethostbyname`
3. Puts every port of the range in a `Queue`
4. Starts N worker threads; each one takes ports from the queue and tries a TCP connect (`socket.connect`, 5 s timeout)
5. Prints each open port as it is found, then a summary

Threads make the scan much faster than a sequential loop, and the `Queue` makes sure no two threads scan the same port.

| Range option | Ports |
| --- | --- |
| Well-known | 1 to 1024 |
| Registered | 1025 to 49152 |
| Dynamic | 49153 to 65535 |
| All | 1 to 65535 |

## Usage

```bash
pip install inquirer
python PortScanner.py
```

Demo video (Portuguese): https://youtu.be/dRBEl9ykL_Y

## Legal notice

Only scan hosts you own or have explicit written permission to test. Unauthorized port scanning may be illegal and violate network policies.

## What I would improve today

- Close sockets properly and handle unknown services without errors
- Add command-line arguments (`argparse`) for non-interactive use
- Add a UDP scan mode and banner grabbing
- Use `asyncio` instead of threads for very large ranges
- Export results to JSON or CSV
