import subprocess
import os
import sys

from bot_python_sdk.store import Store
from bot_python_sdk.key_generator import KeyGenerator

if not Store().has_config():
    if len(sys.argv) <= 1:
        exit('Please add your makerID to configure the SDK: "python server.py YOUR_MAKER_ID"')
    maker_id = sys.argv[1]

    key_generator = KeyGenerator()
    key_generator.generate_key()
    public_key = key_generator.public_key()
    private_key = key_generator.private_key()
    uuid = key_generator.generate_uuid()

    Store().store_config(maker_id, uuid, private_key, public_key)

# If OS is windows based, it doesn't support gunicorn so we run waitress
if os.name == 'nt':
    subprocess.Popen(['waitress-serve', '--port=3001', 'bot_python_sdk.api:api'])
else:
    subprocess.Popen(['gunicorn', '-b', '127.0.0.1:3001', 'bot_python_sdk.api:api'])
