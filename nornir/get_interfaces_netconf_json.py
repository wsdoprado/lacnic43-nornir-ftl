#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

from nornir import InitNornir
from dotenv import load_dotenv
from nornir_netconf.plugins.tasks import netconf_get_config
from nornir.core.exceptions import NornirExecutionError
import os
import json
import xmltodict

# Load environment variables from .env file
load_dotenv()

NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
NETBOX_URL = os.getenv("NETBOX_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def get_interfaces_netconf(task):
    try:
        # Run NETCONF get-config operation
        data_interfaces = task.run(
            netconf_get_config,
            source="running",
            path="""
            <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
            </interface-configurations>
            """,
            filter_type="subtree",
        )

        # Parse the XML result into a Python dictionary
        obj = xmltodict.parse(data_interfaces.result.rpc.data_xml)
        json_interfaces = json.loads(json.dumps(obj.get('data', {})))

        print(f"Accessing host: {task.host}")
        interfaces = json_interfaces.get('interface-configurations', {}).get('interface-configuration', [])

        # Normalize single interface object to list
        if isinstance(interfaces, dict):
            interfaces = [interfaces]

        for interface in interfaces:
            print(json.dumps(interface, indent=2))

    except Exception as e:
        task.host["error"] = str(e)
        print(f"[ERROR] Failed to get interfaces from host {task.host}: {e}")


try:
    # Initialize Nornir with threaded runner and NetBox inventory
    nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": NETBOX_URL,
                "nb_token": NETBOX_TOKEN,
                "filter_parameters": {
                    "region": "br",
                    "site": ["ce", "sp"],
                    "status": "active",
                    "platform": "iosxr"
                },
                "ssl_verify": False
            }
        }
    )

    nr.inventory.defaults.username = USERNAME
    nr.inventory.defaults.password = PASSWORD
    nr.inventory.defaults.port = 830

    # Run the NETCONF interface task
    result = nr.run(task=get_interfaces_netconf)

    # Optionally, print any hosts that had errors
    #print("\n[SUMMARY OF ERRORS]")
    #for host, r in result.items():
    #    if r.failed or "error" in host.data:
    #        print(f"- {host}: {host.get('error', 'Task failed')}")

except NornirExecutionError as e:
    print(f"[ERROR] Nornir execution failed: {str(e)}")

except Exception as e:
    print(f"[ERROR] Unexpected error occurred: {str(e)}")
