from bot_python_sdk.action_service import ActionService
from bot_python_sdk.action_service import ACTION_ID, DEVICE_ID, QUEUE_ID, VALUE, ALTERNATIVE_ID
from unittest.mock import patch

@patch('bot_python_sdk.configuration.Configuration.get_device_id')
@patch('bot_python_sdk.key_generator.KeyGenerator.generate_uuid')
def test_create_trigger_body(generate_uuid, get_device_id):

	as_obj = ActionService()

	uuid = 42
	generate_uuid.return_value = uuid
	device_id = 43
	get_device_id.return_value = device_id
	action_id = '44'
	alt_id = '45'
	value = '46'

	trigger_body = {
            ACTION_ID: action_id,
            DEVICE_ID: device_id,
            QUEUE_ID: uuid,
            ALTERNATIVE_ID: alt_id,
            VALUE: value
		}

	assert as_obj.create_trigger_body(action_id, value, alt_id) == trigger_body

