#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

from nornir import InitNornir
from dotenv import load_dotenv
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
import os

#Load the data on the .env file
load_dotenv()

NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
NETBOX_URL = os.getenv("NETBOX_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": NETBOX_URL,
                "nb_token": NETBOX_TOKEN,
                "filter_parameters": {"region": "br", "site": ["ce"], "status": "active", "platform": "iosxr"},
                "ssl_verify": False}
        })

nr.inventory.defaults.username = USERNAME
nr.inventory.defaults.password = PASSWORD

print_result(nr.run(task=napalm_get, getters=["get_interfaces"]), vars=["result"])






