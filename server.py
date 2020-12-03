import sys

from bot_python_sdk.finn import Finn
from bot_python_sdk.util.logger import Logger
from bot_python_sdk.data.storage import Storage


###
# Class Server
# Started with 'make server' user input
##

# Request user input
def __initialize_configuration(product_id):
    Logger.info('Server', 'initialize_configuration product_id = ' + product_id)

    # Option for Multi pairing
    # If the option is yes, then alternative id needed
    is_multi_pair = False
    aid = ''
    if input('Enable Multi pair(yes/no)') == 'yes':
        is_multi_pair = True
        aid = input('Enter device alternative identifier displayname:')

    bluetooth_enabled = False
    if input('Enable Bluetooth (yes/no; default is yes)') == 'yes':
        bluetooth_enabled = True

    Logger.info('Server', 'initialize_configuration done')
    Finn(product_id, is_multi_pair, aid, bluetooth_enabled, None)


# Resume Finn or generate configuration
if Storage.has_configuration():
    Finn(None, None, None, None, None)
else:
    # argv comes from Makefile
    # argv 1 is server.py
    # argv 2 is input after productID=

    if len(sys.argv) != 2:
        exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
    elif len(sys.argv[1]) != 36:
        exit('Please enter a valid productID')
    else:
        # argv is the console input
        __initialize_configuration(sys.argv[1])
