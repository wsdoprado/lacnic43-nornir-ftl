#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks.netmiko_send_command import netmiko_send_command

nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 20}},
    config_file="./config.yaml"
)

results = nr.run(netmiko_send_command, read_timeout=120, command_string="show interfaces brief")

print_result(results)



