import falcon

class BotServerError(falcon.HTTPError):
    def __init__(self, code, description, message):
        self._errorCode = code
        self._errorDescription = description
        self._errorMessage = message
        super().__init__(code, description = description)

    def to_dict(self, obj_type=dict):
        result = super().to_dict(obj_type)
        result['code'] = self._errorCode
        result['message'] = self._errorMessage
        return result
