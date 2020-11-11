import datetime

# Console colors
COLOR_INFO = '\x1b[39m'  # Default color, depends on console settings
COLOR_SUCCESS = '\x1b[32m'  # Green
COLOR_WARNING = '\x1b[33m'  # Yellow
COLOR_ERROR = '\x1b[31m'  # Red
DELIMITER = ': '


class Logger:
    @staticmethod
    def info(location, message):
        print(Logger.timestamp() + location + DELIMITER + message)

    @staticmethod
    def success(location, message):
        print(Logger.timestamp() + COLOR_SUCCESS + location + DELIMITER + message + COLOR_INFO)

    @staticmethod
    def warning(location, message):
        print(Logger.timestamp() + COLOR_WARNING + location + DELIMITER + message + COLOR_INFO)

    @staticmethod
    def error(location, message):
        print(Logger.timestamp() + COLOR_ERROR + location + DELIMITER + message + COLOR_INFO)

    @staticmethod
    def timestamp():
        return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
