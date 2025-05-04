#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10


from load_environment import load_environment
from nornir_setup import init_nornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


def main():
    env = load_environment()
    nr = init_nornir(env)

    print("\n📡 Retrieving Interface Data via NAPALM...\n")
    results = nr.run(task=napalm_get, getters=["get_interfaces"])
    print_result(results, vars=["result"])


if __name__ == "__main__":
    main()


