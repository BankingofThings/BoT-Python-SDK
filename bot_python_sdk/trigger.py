import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.store import Store


class Trigger:
    def __init__(self, action_id, value=None):
        self.action_id = action_id
        self.value = value

    def send(self):
        success = BoTService().trigger_action(self.action_id, self.value)
        if success:
            Store().set_last_triggered(self.action_id, time.time())
        return success

    def frequency_is_valid(self):
        last_triggered = Store().get_last_triggered(self.action_id)
        return True if last_triggered == 'never' else self.can_trigger(last_triggered)

    def can_trigger(self, last_triggered):
        action = self.get_action()
        if not action:
            return False

        frequency = action['frequency']
        now = time.time()

        # This is beautiful code
        if frequency == 'yearly':
            return now - last_triggered > 3600 * 24 * 7 * 52
        if frequency == 'half-yearly':
            return now - last_triggered > 3600 * 24 * 7 * 26
        if frequency == 'monthly':
            return now - last_triggered > 3600 * 24 * 7 * 4
        if frequency == 'weekly':
            return now - last_triggered > 3600 * 24 * 7
        if frequency == 'daily':
            return now - last_triggered > 3600 * 24
        if frequency == 'hourly':
            return now - last_triggered > 3600
        if frequency == 'minutely':
            return now - last_triggered > 60
        return True

    def get_action(self):
        actions = Store().get_actions()
        for action in actions:
            if action['name'] == self.action_id:
                return action
        print('Could not find action...')
        return False
