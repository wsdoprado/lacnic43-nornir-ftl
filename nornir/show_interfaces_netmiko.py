#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10


from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.task import Task, Result


def send_command_with_error_handling(task: Task) -> Result:
    """
    Executes a Netmiko command and handles errors gracefully.
    """
    try:
        response = task.run(
            task=netmiko_send_command,
            command_string="show interfaces brief",
            read_timeout=120
        )
        return Result(
            host=task.host,
            result=response.result
        )
    except Exception as e:
        return Result(
            host=task.host,
            result=f"❌ Error: {str(e)}",
            failed=True
        )


def main():
    # Initialize Nornir with config and threaded runner
    nr = InitNornir(
        config_file="./config.yaml",
        runner={"plugin": "threaded", "options": {"num_workers": 20}}
    )

    # Run the task across all devices
    results = nr.run(task=send_command_with_error_handling)

    # Print results, including any errors
    print_result(results)


if __name__ == "__main__":
    main()
