import pytest
import falcon
import json
from bot_python_sdk.store import Store
from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.bot_server_error import BotServerError
from bot_python_sdk.configuration_store import ConfigurationStore

configuration_store = ConfigurationStore()
configuration = configuration_store.get()
key_generator = KeyGenerator()

def test_get_actions_with_empty_configuration():
    #Test should fail with 401 Unauthorized error

    #Reset configuration
    Store.remove_configuration()

    with pytest.raises(BotServerError) as unauthorizedExceptionInfo:
        bot_service = BoTService()
        bot_service.get("/actions")

    assert '401' in str(unauthorizedExceptionInfo.value)

def test_get_actions_with_wrong_maker_id():
    #Test should fail with 401 Unauthorized error

    #Reset configuration
    Store.remove_configuration()

    #Initialize device configuration missing makerId value
    configuration.initialize("wrong-maker-id", key_generator.generate_uuid(), DeviceStatus.NEW.value, False, None, None,None)
    configuration_store.save(configuration)

    with pytest.raises(BotServerError) as badRequestExceptionInfo:
        bot_service = BoTService()
        bot_service.get("/actions")

    assert '401' in str(badRequestExceptionInfo.value)

def test_get_actions_with_correct_product_id():
    #Test should success with 200

    #Reset configuration
    Store.remove_configuration()

    #Initialize with values
    product_id = '4E87156E-A7F2-4AD8-BC6E-B4F73D39C218'
    device_id = '5e6a629e-4f08-4918-a50a-8c3a8f0d58f1'

    #Initialize device configuration missing makerId value
    configuration.initialize(product_id, device_id, DeviceStatus.PAIRED.value, False, None, None,None)
    configuration_store.save(configuration)

    #Expected values in actions
    action_id = '77ED91B7-253C-4D81-B287-EB17E6166C5D'
    action_name = 'Capiccino'

    #Make call to BoT Server
    bot_service = BoTService()
    actions = bot_service.get("/actions")

    #Validate the retruned actions set
    assert action_id in json.dumps(actions)
    assert action_name in json.dumps(actions)
