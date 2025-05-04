#!/opt/lacnic43-nornir-ftl/venv/bin/python3.10


from nornir import InitNornir


def init_nornir(env: dict):
    """
    Initializes Nornir with NetBox inventory.
    """

    nr =  InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": env['nb_url'],
                "nb_token": env['nb_token'],
                "filter_parameters": {
                    "region": "br",
                    "site": ["ce", "rj", "sp"],
                    "status": "active",
                    "platform": "iosxr"
                },
                "ssl_verify": False
            }
        }
    )

    nr.inventory.defaults.username = env['user']
    nr.inventory.defaults.password = env['passw']

    return nr


