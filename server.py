import sys

from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store


###
# Class Server
# Started with 'make server' user input
##

# Request user input
def initialize_configuration(product_id):
    Logger.info('Server', 'initialize_configuration product_id = ' + product_id)

    # Option for Multi pairing
    # If the option is yes, then alternative id needed
    device_status = DeviceStatus.NEW
    aid = ''
    if input('Enable Multi pair(yes/no)') == 'yes':
        device_status = DeviceStatus.MULTIPAIR
        aid = input('Enter your alternativeID:')

    bluetooth_enabled = False
    if input('Enable Bluetooth (yes/no; default is yes)') == 'yes':
        bluetooth_enabled = True

    Logger.info('Server', 'initialize_configuration done')
    Finn(product_id, device_status, aid, bluetooth_enabled, None)


# Resume Finn or generate configuration
if Store.has_configuration():
    Finn(None, None, None, None, None)
else:
    if len(sys.argv) != 2:
        exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
    elif len(sys.argv[1]) != 36:
        exit('Please enter a valid productID')
    else:
        # argv is the console input
        initialize_configuration(sys.argv[1])
