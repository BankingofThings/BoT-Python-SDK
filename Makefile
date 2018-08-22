install: ; pip install --upgrade setuptools && pip install -r requirements.txt

server: ; python server.py $(makerID)

activate: ; python -c "from bot_python_sdk.polling_service import PollingService; PollingService().run()"

test: ; pytest

environment: ; sudo pip install virtualenv && virtualenv venv
