import json

from bot_python_sdk.services.service_bot_talk import BotTalkModel


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

    @staticmethod
    def create_bot_talk_model(payload):
        payload_object = json.loads(payload['payload'])
        return BotTalkModel(payload_object['actionID'], payload_object['customerID'])
