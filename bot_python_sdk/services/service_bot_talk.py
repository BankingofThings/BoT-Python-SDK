import json

from bot_python_sdk.util.logger import Logger
from bot_python_sdk.util.pojo_converter import PojoConverter


class BotTalkService:
    def __init__(self, bot_service):
        Logger.info('BotTalkService', '__init__')
        self.__bot_service = bot_service

    def execute(self):
        try:
            response = self.__bot_service.get('messages')

            if response is not None:
                return PojoConverter.create_bot_talk_model(response)
            else:
                return None
        except Exception as e:
            Logger.info('BotTalkService', 'start error:' + str(e))
            return None


class BotTalkModel:
    def __init__(self, action_id, customer_id):
        Logger.info('BotTalkModel', '__init__\nactionID=' + action_id + "\ncustomerID=" + customer_id)
        self.action_id = action_id
        self.customer_id = customer_id
