#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10


from load_environment import load_environment
from nornir_setup import init_nornir
from nornir_netconf.plugins.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError


def run_netconf_task(nr):
    """
    Runs NETCONF get-config on the configured hosts to retrieve interface configurations.
    """

    nr.inventory.defaults.port = 830  # Standard NETCONF port

    return nr.run(
        task=netconf_get_config,
        source="running",
        path="""
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        </interface-configurations>
        """,
        filter_type="subtree"
    )


def main():
    try:
        print("🚀 Starting NETCONF configuration retrieval...")

        env = load_environment()
        nr = init_nornir(env)
        results = run_netconf_task(nr)

        print_result(results)

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

    

