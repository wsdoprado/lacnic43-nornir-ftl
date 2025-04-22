#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

from load_environment import load_environment
from nornir_setup import init_nornir

def display_inventory(nr):
    """
    Displays all hosts and their group associations.
    """
    print("\n📋 Inventory Hosts and Their Groups:\n")
    for host in nr.inventory.hosts.values():
        groups = [group.name for group in host.groups]
        print(f"- {host.name}: {host.hostname} | Groups: {groups}")
    print()


def main():
    # Load env file with credentials
    env = load_environment()

    # Start Nornir Framework
    nr = init_nornir(env) 

    # Run display_inventory task
    display_inventory(nr)


if __name__ == "__main__":
    main()



