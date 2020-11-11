from bot_python_sdk.util.logger import Logger


class BotTalkService:
    def __init__(self, bot_service):
        Logger.info('BotTalkService', '__init__')
        self.__bot_service = bot_service

    def execute(self):
        try:
            return self.__bot_service.get('messages')
        except Exception as e:
            Logger.info('BotTalkService', 'start error:' + str(e))
            return None
