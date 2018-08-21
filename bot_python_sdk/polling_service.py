import time

from bot_python_sdk.bot_service import BoTService


class PollingService:
    POLLING_INTERVAL_IN_SECONDS = 5
    MAXIMUM_TRIES = 24

    def run(self):
        print('Polling to activate this device...')
        tries = 0
        activated = BoTService().activate()
        while not activated:
            tries += 1

            if tries >= self.MAXIMUM_TRIES:
                break

            time.sleep(self.POLLING_INTERVAL_IN_SECONDS)

            print('Activating device, attempt ' + str(tries + 1))
            activated = BoTService().activate()

        print('Device activated!' if activated else 'Could not activate device, tried ' + str(tries) + ' times')
