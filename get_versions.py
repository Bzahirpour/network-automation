#!/usr/bin/env python3
"""
get_versions.py
Connects to network devices defined in inventory.yaml and retrieves
software version information using NAPALM. Outputs results to terminal
and saves a CSV report.
"""

import yaml
import napalm
import csv
import os
from tabulate import tabulate
from getpass import getpass
from datetime import datetime


def load_inventory(filename="inventory.yaml"):
    """Load device inventory from YAML file."""
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def get_credentials():
    """Prompt user for credentials once and reuse across all devices."""
    print("Enter device credentials:")
    username = input("Username: ")
    password = getpass("Password: ")
    return username, password


def get_device_facts(device, username, password):
    """Connect to a device and retrieve facts using NAPALM."""
    driver = napalm.get_network_driver(device["driver"])

    connection = driver(
        hostname=device["ip"],
        username=username,
        password=password,
    )

    try:
        print(f"Connecting to {device['name']} ({device['ip']})...")
        connection.open()
        facts = connection.get_facts()
        connection.close()

        return {
            "Device": device["name"],
            "Vendor": facts["vendor"],
            "Model": facts["model"],
            "OS Version": facts["os_version"],
            "Uptime (s)": facts["uptime"],
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "OK",
        }

    except Exception as e:
        try:
            connection.close()
        except:
            pass
        return {
            "Device": device["name"],
            "Vendor": "N/A",
            "Model": "N/A",
            "OS Version": "N/A",
            "Uptime (s)": "N/A",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": f"FAILED: {str(e).splitlines()[0]}",
        }

def save_csv(results):
    """Save results to a timestamped CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"software_inventory_{timestamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nReport saved to {filename}")
    return filename


def main():
    inventory = load_inventory()
    devices = inventory["devices"]

    username, password = get_credentials()

    results = []
    for device in devices:
        facts = get_device_facts(device, username, password)
        results.append(facts)

    print("\n" + "=" * 80)
    print("NETWORK DEVICE SOFTWARE INVENTORY")
    print("=" * 80)
    print(tabulate(results, headers="keys", tablefmt="grid"))

    save_csv(results)


if __name__ == "__main__":
    main()