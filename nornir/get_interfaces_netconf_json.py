#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

"""
Script: netconf_get_config_interfaces.py
Description: Retrieves interface configuration via NETCONF using Nornir, NetBoxInventory2, and Cisco IOS-XR YANG models.
Author: William Prado
Email: wprado@nic.br | wsprado@outlook.com
"""

import os, json, xmltodict
from dotenv import load_dotenv
from nornir import InitNornir
from nornir_netconf.plugins.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError


def load_environment() -> dict:
    """
    Loads and validates required environment variables from .env file.
    """
    load_dotenv()
    required_vars = ["NETBOX_TOKEN", "NETBOX_URL", "USERNAME", "PASSWORD"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return {
        "netbox_token": os.getenv("NETBOX_TOKEN"),
        "netbox_url": os.getenv("NETBOX_URL"),
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }


def init_nornir(env: dict):
    """
    Initializes Nornir with NetBoxInventory2 and applies default credentials.
    """
    nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": env["netbox_url"],
                "nb_token": env["netbox_token"],
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

    nr.inventory.defaults.username = env["username"]
    nr.inventory.defaults.password = env["password"]
    nr.inventory.defaults.port = 830  # Standard NETCONF port

    return nr


def run_netconf_task(nr):
    """
    Runs NETCONF get-config on the configured hosts and returns JSON-converted results.
    """
    raw_results = nr.run(
        task=netconf_get_config,
        source="running",
        path="""
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        </interface-configurations>
        """,
        filter_type="subtree"
    )

    # Convert XML result to JSON-like dict using xmltodict
    for host, result in raw_results.items():
        if not result.failed:
            try:
                xml_data = result.result.rpc.data_xml
                parsed = xmltodict.parse(xml_data)
                json_output = json.dumps(parsed, indent=2)
                print(f"\n📦 JSON Output for host {host}:\n{json_output}\n")
            except Exception as e:
                print(f"[ERROR] Failed to parse XML for {host}: {e}")
        else:
            print(f"[FAIL] Host {host} returned a failure status.")

    return raw_results


def main():
    try:
        print("🚀 Starting NETCONF configuration retrieval...")
        env = load_environment()
        nr = init_nornir(env)
        results = run_netconf_task(nr)

        failed_hosts = [host for host, r in results.items() if r.failed]
        if failed_hosts:
            print("\n⚠️  The following hosts failed during NETCONF execution:")
            for host in failed_hosts:
                print(f"- {host}")

    except NornirExecutionError as e:
        print(f"[ERROR] Nornir execution failed: {str(e)}")
    except EnvironmentError as e:
        print(f"[ERROR] Environment issue: {str(e)}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()

