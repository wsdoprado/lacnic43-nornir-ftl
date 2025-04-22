# 🤖 Nornir - Python Framework for Network Automation

This project leverages the **[Nornir](https://nornir.tech/)** framework to automate network tasks using Python. Nornir provides a scalable and customizable approach to network automation, enabling you to manage multiple devices programmatically and efficiently.

## ⚡ Overview

With this project, you can:

- Automate SSH connections to multiple devices simultaneously
- Run remote commands on switches and routers
- Collect configurations and interface statuses

## 🛠️ Technologies Used

- Python 3.10
- [Nornir](https://nornir.tech/)
- [NAPALM](https://napalm.readthedocs.io/) (optional)
- [Netmiko](https://github.com/ktbyers/netmiko)
- [Rich](https://github.com/Textualize/rich) (for logging and CLI output)
- [Pandas](https://pandas.pydata.org/) (for data processing and reports)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (for environment variable management)

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/wsdoprado/lacnic43-nornir-ftl.git
   cd lacnic43-nornir-ftl

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Create a .env file in the root directory and add your credentials:
   ```ini
   NETBOX_URL="http://localhost:8000/"
   NORNIR_TOKEN=
   USERNAME="lacnic"
   PASSWORD="lacnic"
5. Configure your Nornir inventory under inventory/:

    hosts.yaml

    groups.yaml

    defaults.yaml

6. Run the show_inventory.py script:
   ```bash
    python main.py


🤝 Contributing

Contributions are welcome! Feel free to open an issue, fork the project, or submit a pull request.
📄 License

This project is licensed under the MIT License.

Made with 🧠 by Your Name
   
