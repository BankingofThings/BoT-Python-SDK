from bot_python_sdk.services.action_service import ActionService
from unittest.mock import patch

from bot_python_sdk.services.bot_service import BoTService
from bot_python_sdk.data.configuration import Configuration
from bot_python_sdk.util.pojo_converter import PojoConverter


@patch('bot_python_sdk.data.configuration.Configuration.get_device_id')
def test_create_trigger_body(get_device_id):
    action_id = '44'
    device_id = '43'
    queue_id = 42
    alt_id = '45'
    value = '46'

    get_device_id.return_value = device_id

    expected_result = {
        'actionID': action_id,
        'deviceID': device_id,
        'queueID': queue_id,
        'alternativeID': alt_id,
        'value': value
    }

    actual_result = PojoConverter.create_trigger_body(action_id, device_id, queue_id, alt_id, value)

    assert actual_result == expected_result
