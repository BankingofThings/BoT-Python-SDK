install: ; pip install --upgrade setuptools && pip install -r requirements.txt

server: ; python server.py $(makerID)

activate: ; python -c "from bot_python_sdk.polling_service import PollingService; PollingService().run()"

test: ; pytest

environment-alpine: ; pip install --user virtualenv && virtualenv venv && sudo apk add gcc musl-dev python3-dev libffi-dev openssl-dev

environment-debian: ; pip install --user virtualenv && virtualenv venv && sudo apt-get install build-essential libssl-dev libffi-dev python3-dev

environment-RHEL: pip install --user virtualenv && virtualenv venv && sudo yum install redhat-rpm-config gcc libffi-devel python-devel openssl-devel

environment-osx: ; pip install virtualenv && virtualenv venv

environment-windows: ; pip install virtualenv && virtualenv venv
