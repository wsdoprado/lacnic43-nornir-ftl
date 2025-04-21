#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

from nornir import InitNornir
from dotenv import load_dotenv
import os

#Load the data on the .env file
load_dotenv()

NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
NETBOX_URL = os.getenv("NETBOX_URL")

nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": NETBOX_URL,
                "nb_token": NETBOX_TOKEN,
                "filter_parameters": {"region": "br", "site": ["ce","rj","sp"], "status": "active", "platform": "iosxr"},
                "ssl_verify": False}
        })

# Exibe os hosts e seus grupos
print("\n📋 Hosts do Inventário e seus Grupos:\n")
for host in nr.inventory.hosts.values():
    groups = [g.name for g in host.groups]
    print(f"- {host.name}: {host.hostname} | Grupos: {groups}")

print("\n")


