from bot_python_sdk.util.key_generator import KeyGenerator


class PojoConverter:

    @staticmethod
    def create_trigger_body(action_id, device_id, queue_id, alternative_id, value):
        data = {
            'actionID': action_id,
            'deviceID': device_id,
            'queueID': queue_id
        }

        if alternative_id is not None:
            data['alternativeID'] = str(alternative_id)
        if value is not None:
            data['value'] = str(value)
        return data
