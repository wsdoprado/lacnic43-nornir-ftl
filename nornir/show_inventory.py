#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10
"""
Script to display hosts from the Nornir inventory along with their respective groups.
"""

from nornir import InitNornir


def main():
    # Initialize Nornir with config file and threaded runner
    nr = InitNornir(
        config_file="./inventory/config.yaml",
        runner={"plugin": "threaded", "options": {"num_workers": 20}}
    )

    print("\n📋 Inventory Hosts and Their Groups:\n")

    for host in nr.inventory.hosts.values():
        group_names = [group.name for group in host.groups]
        print(f"- {host.name}: {host.hostname} | Groups: {group_names}")

    print()


if __name__ == "__main__":
    main()

