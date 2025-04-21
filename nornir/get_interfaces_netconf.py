#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

from nornir import InitNornir
from dotenv import load_dotenv
from nornir_netconf.plugins.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError
import os

# Load environment variables from the .env file
load_dotenv()

NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
NETBOX_URL = os.getenv("NETBOX_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

try:
    # Initialize Nornir
    nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": NETBOX_URL,
                "nb_token": NETBOX_TOKEN,
                "filter_parameters": {
                    "region": "br",
                    "site": ["ce"],
                    "status": "active",
                    "platform": "iosxr"
                },
                "ssl_verify": False
            }
        }
    )

    # Set default NETCONF credentials
    nr.inventory.defaults.username = USERNAME
    nr.inventory.defaults.password = PASSWORD
    nr.inventory.defaults.port = 830  # Use int for consistency

    # Execute the NETCONF get-config task
    result = nr.run(
        netconf_get_config,
        source="running",
        path="""
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        </interface-configurations>
        """,
        filter_type="subtree",
    )

    # Print results
    print_result(result)

    # Check for any failed hosts
    failed_hosts = [host for host, r in result.items() if r.failed]
    if failed_hosts:
        print("\n[WARNING] The following hosts failed during execution:")
        for host in failed_hosts:
            print(f"- {host}")
    
except NornirExecutionError as e:
    print(f"[ERROR] Nornir execution failed: {str(e)}")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {str(e)}")