import os
import subprocess
import sys

from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.store import Store

configuration_service = ConfigurationService()
store = Store()

if not store.has_configuration():
    if len(sys.argv) <= 1:
        exit('Please add your makerID to configure the SDK: "make server makerID=YOUR_MAKER_ID"')
    maker_id = sys.argv[1]  # 1 -> First argument after server.py
    configuration_service.initialize_configuration(maker_id)

# If OS is windows based, it doesn't support gunicorn so we run waitress
if os.name == 'nt':
    subprocess.run(['waitress-serve', '--port=3001', 'bot_python_sdk.api:api'])
else:
    subprocess.run(['gunicorn', '-b', '127.0.0.1:3001', 'bot_python_sdk.api:api'])
