import falcon

from bot_python_sdk.finn import Finn

# Triggered by gunicorn
# Start Webserver and add supported endpoint resources
api = application = falcon.API()

# Start finn
Finn(api)
