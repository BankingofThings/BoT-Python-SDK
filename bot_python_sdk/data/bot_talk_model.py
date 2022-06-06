from bot_python_sdk.util.logger import Logger


class BotTalkModel:
    def __init__(self, action_id, customer_id):
        Logger.info('BotTalkModel', '__init__\nactionID=' + action_id + "\ncustomerID=" + customer_id)
        self.action_id = action_id
        self.customer_id = customer_id
