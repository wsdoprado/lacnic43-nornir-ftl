#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10


from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result


def show_inventory(task: Task) -> Result:
    """
    Returns the host's name and IP address.
    """
    return Result(
        host=task.host,
        result=f"Name: {task.host.name} - IP Address: {task.host.hostname}"
    )


def main():
    # Initialize Nornir using the config.yaml file with threaded execution
    nr = InitNornir(
        config_file="./config.yaml",
        runner={"plugin": "threaded", "options": {"num_workers": 20}}
    )

    # Execute the task and print the results
    result = nr.run(task=show_inventory)
    print_result(result)


if __name__ == "__main__":
    main()

