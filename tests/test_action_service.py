from bot_python_sdk.action_service import ActionService
from unittest.mock import patch


@patch('bot_python_sdk.configuration.Configuration.get_device_id')
@patch('bot_python_sdk.key_generator.KeyGenerator.generate_uuid')
def test_create_trigger_body(generate_uuid, get_device_id):
    __actionService = ActionService()

    action_id = '44'
    device_id = '43'
    uuid = 42
    alt_id = '45'
    value = '46'

    generate_uuid.return_value = uuid
    get_device_id.return_value = device_id

    trigger_body = {
        'actionID': action_id,
        'deviceID': device_id,
        'queueID': uuid,
        'alternativeID': alt_id,
        'value': value
    }

    assert __actionService._create_trigger_body(action_id, value, alt_id) == trigger_body
