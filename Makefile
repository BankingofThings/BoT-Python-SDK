install: ; pip install --upgrade pip && pip install --upgrade setuptools && pip install -r requirements.txt

server: ; python3 server.py $(makerID)

activate: ; python3 -c "from bot_python_sdk.polling_service import PollingService; PollingService().run()"

test: ; pytest

environment-raspberry: ; python3 -m venv venv && sudo apt-get install build-essential libssl-dev libffi-dev python3-dev

environment-osx: ; python3 -m venv venv

environment-windows: ; python3 -m venv venv
