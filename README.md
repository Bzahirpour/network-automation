# Network Device Software Inventory

A Python script that connects to network devices and retrieves software version 
information using NAPALM (Network Automation and Programmability Abstraction Layer 
with Multivendor support). Results are displayed in a formatted table and exported 
to a timestamped CSV report.

## Supported Vendors
- Juniper (JunOS) — MX, SRX
- Cisco (IOS/IOS-XE) — Routers and Switches

## Requirements
- Python 3.x
- See requirements.txt for full dependency list

## Installation

Clone the repository and set up a virtual environment:
```bash
git clone https://github.com/yourusername/network-automation.git
cd network-automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Update `inventory.yaml` with your device details then run:
```bash
python get_versions.py
```

You will be prompted for credentials once — they are reused across all devices 
and never stored to disk.

## Inventory File
```yaml
devices:
  - name: site1-mx1
    ip: 192.168.1.1
    driver: junos

  - name: site2-sw1
    ip: 192.168.1.2
    driver: ios
```

## Drivers
- `junos` — Juniper (connects via NETCONF/PyEZ)
- `ios` — Cisco IOS/IOS-XE (connects via SSH/Netmiko)
- `nxos` — Cisco NX-OS
- `eos` — Arista

## Output

Results are displayed in the terminal and saved as a timestamped CSV file:
```
================================================================================
NETWORK DEVICE SOFTWARE INVENTORY
================================================================================
+--------------------+--------+--------+-------------------+------------+---------------------+--------+
| Device             | Vendor | Model  | OS Version        | Uptime (s) | Timestamp           | Status |
+--------------------+--------+--------+-------------------+------------+---------------------+--------+
| site1-mx1          | Juniper| MX204  | 23.2R2            | 86400      | 2026-03-21 18:00:00 | OK     |
| site2-sw1          | Cisco  | C8000V | Version 17.15.4c  | 8880       | 2026-03-21 18:00:00 | OK     |
+--------------------+--------+--------+-------------------+------------+---------------------+--------+
```

## Notes
- Credentials are prompted at runtime and never stored
- Failed connections are captured in the report with a FAILED status
- CSV output files are excluded from version control