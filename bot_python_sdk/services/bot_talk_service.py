from bot_python_sdk.util.logger import Logger
from bot_python_sdk.util.pojo_converter import PojoConverter


class BotTalkService:
    def __init__(self, bot_service):
        Logger.info('BotTalkService', '__init__')
        self.__bot_service = bot_service

    def execute(self):
        try:
            response = self.__bot_service.get('messages')

            if response.status_code is not 204:
                Logger.info('BotTalkService', 'execute message received')
                return PojoConverter.create_bot_talk_model(response)
            else:
                Logger.info('BotTalkService', 'execute no message')
                return None
        except Exception as e:
            Logger.info('BotTalkService', 'start error:' + str(e))
            return None
