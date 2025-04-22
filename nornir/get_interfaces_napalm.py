#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10


import os
from dotenv import load_dotenv
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


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

    return nr


def main():
    env = load_environment()
    nr = init_nornir(env)

    print("\n📡 Retrieving Interface Data via NAPALM...\n")
    results = nr.run(task=napalm_get, getters=["get_interfaces"])
    print_result(results, vars=["result"])


if __name__ == "__main__":
    main()


