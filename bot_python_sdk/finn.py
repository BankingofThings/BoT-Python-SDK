import json
import subprocess
import time

import qrcode
from cryptography.fernet import Fernet
from qrcode.image.pure import PymagingImage

from bot_python_sdk.data.configuration import Configuration
from bot_python_sdk.data.device_status import DeviceStatus
from bot_python_sdk.data.storage import Storage
from bot_python_sdk.resources.actions_resource import ActionsResource
from bot_python_sdk.resources.base_resource import BaseResource
from bot_python_sdk.resources.pairing_resource import PairingResource
from bot_python_sdk.resources.qr_code_resource import QRCodeResource
from bot_python_sdk.services.action_service import ActionService
from bot_python_sdk.services.activate_device_service import ActiveDeviceService
from bot_python_sdk.services.bluetooth_service import BluetoothService
from bot_python_sdk.services.bot_service import BoTService
from bot_python_sdk.services.bot_talk_service import BotTalkService
from bot_python_sdk.services.pairing_service import PairingService
from bot_python_sdk.util.key_generator import KeyGenerator
from bot_python_sdk.util.logger import Logger
from bot_python_sdk.util.utils import Utils


class Finn:
    def __init__(self, product_id, device_status, aid, bluetooth_enabled, api):
        Logger.info('Finn', '__init__')

        # Server started, just continue with Finn.init
        if api is not None:
            self.__configuration = Storage.get_configuration_object()

            Logger.info('Finn', '__init__ server created productID =' + self.__configuration.product_id + ', deviceID = ' + self.__configuration.device_id)

            self.__bot_service = BoTService(self.__configuration.private_key, self.__configuration.get_headers())
            self.__action_service = ActionService(self.__configuration, self.__bot_service, self.__configuration.device_id)
            self.__pairing_service = PairingService(self.__bot_service)
            self.__activate_device_service = ActiveDeviceService(self.__bot_service, self.__configuration.get_device_id())
            self.__bot_talk_service = BotTalkService(self.__bot_service)

            self.__init_api(api)

            self.__process_device_status()
        # New install, no configuration, just create configuration and start server
        elif product_id is not None:
            Logger.info('Finn', '__init__ creating config bluetooth_enabled = ' + str(bluetooth_enabled))
            public_key, private_key = KeyGenerator.generate_key()
            device_id = KeyGenerator.generate_uuid()
            # Added alternative id as an argument to initializing the configuration
            Storage.store_aes_key(Fernet.generate_key())
            self.__configuration = Configuration()
            self.__configuration.initialize(product_id,
                                            device_id,
                                            device_status,
                                            bluetooth_enabled,
                                            aid,
                                            public_key,
                                            private_key)
            Storage.save_configuration_object(self.__configuration)

            try:
                Storage.save_qrcode(qrcode.make(json.dumps(Storage.get_device_pojo()), image_factory=PymagingImage))
            except Exception as e:
                Logger.info('ConfigurationService', 'generate_qr_code error:' + str(e))
                raise e

            self.__start_server()
        # We have already configuration, just start server
        else:
            Logger.info('Finn', '__init__ resume device')
            self.__start_server()

    def __process_device_status(self):
        import platform
        system_platform = platform.system()

        Logger.info('Finn', 'init' + ' system_platform = ' + system_platform)

        device_status = self.__configuration.device_status

        if device_status is DeviceStatus.PAIRED:
            Logger.info('Finn', '__init__' + ' Device state is PAIRED, resuming the configuration')
            if self.__activate_device():
                Logger.info('Finn', '__process_device_status device activated')
        else:
            Logger.info('Finn', '__init__' + ' Pair the device either using QRCode or Bluetooth Service through FINN Mobile App')
            if system_platform != 'Darwin' and self.__configuration.is_bluetooth_enabled():
                Logger.info('Finn', '__process_device_status start BLE')
                self.__blue_service = BluetoothService(self.__on_bluetooth_wifi_config_done)


        Logger.info('Finn', '__process_device_status done')

    def __get_actions(self):
        return self.__action_service.get_actions()

    def __activate_device(self):
        return self.__activate_device_service.execute()

    def __start_bot_talk(self):
        bot_talk_model = self.__bot_talk_service.execute()

        if bot_talk_model is not None:
            Logger.info('Finn', '__start_bot_talk message found ' + str(bot_talk_model))

            self.__action_service.trigger(bot_talk_model.action_id, "", bot_talk_model.customer_id)
            self.__start_bot_talk()
        else:
            # run infinite with 5 sec delay. Don't increase delay until CORE supports it.
            time.sleep(5)
            self.__start_bot_talk()

    def __on_bluetooth_wifi_config_done(self):
        self.__pairing_service.stop()

    def __start_server(self):
        Logger.info('Finn', '__start_server')
        # Start application
        # 1. this file
        # 2. gunicorn starts file api.py
        # 3. api.py starts instance of Finn
        __ip_address = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE).communicate()[0].decode('ascii').split(' ')[0]

        Logger.info('Server', "starting with configuration... IP" + __ip_address)

        if Utils.is_valid(__ip_address):
            Logger.info('Server', "Detected IP Address :" + __ip_address)
        else:
            __ip_address = '127.0.0.1'
            Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: " + __ip_address)

        Logger.info('Server', "Starting server at URL: http://" + __ip_address + ':3001/')

        # Executes api.py and indirectly finn.py
        subprocess.run(['gunicorn', '-b', __ip_address + ':3001', 'bot_python_sdk.api:api'])

    # Console api
    def __init_api(self, api):
        Logger.info('Finn', 'init_api')

        api.add_route('/', BaseResource())
        api.add_route('/actions', ActionsResource(self.__action_service))
        api.add_route('/pairing', PairingResource())
        api.add_route('/activate', self.__activate_device_service)
        api.add_route('/qrcode', QRCodeResource())
        api.add_route('/messages', self.__bot_talk_service)
