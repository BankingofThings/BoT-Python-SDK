install: ; sudo pip3 install --upgrade pip && sudo pip3 install --upgrade setuptools && sudo pip3 install -r requirements.txt

server: ; sudo python3 server.py $(makerID)

configuration: ; python3 -c "from bot_python_sdk.configuration_service import ConfigurationService; ConfigurationService().resume_configuration()"

pair: ; python3 -c "from bot_python_sdk.configuration_service import ConfigurationService; ConfigurationService().pair()"

activate: ; python3 -c "from bot_python_sdk.configuration_service import ConfigurationService; ConfigurationService().activate()"

reset: ; python3 -c "from bot_python_sdk.store import Store; Store().remove_configuration()"

qr: ;  python3 -c "from bot_python_sdk.configuration_service import ConfigurationService; ConfigurationService().generate_qr_code()"

test: ; pytest

environment-raspberry: ; sudo apt-get update && sudo apt-get -y install build-essential libssl-dev libffi-dev python3-dev python3-venv && python3 -m venv venv

environment-osx: ; python3 -m venv venv

environment-windows: ; python3 -m venv venv