from bot_python_sdk.data.configuration import Configuration
from bot_python_sdk.data.device_status import DeviceStatus
from bot_python_sdk.data.storage import Storage


def test_has_no_configuration():
    value = Storage.has_configuration()

    assert not value


def test_has_configuration():
    configuration = Configuration()
    configuration.initialize("mi","di",DeviceStatus.PAIRED, True, "aid", "puk", "prk")

    Storage.save_configuration_object(configuration)

    stored_configuration = Storage.get_configuration_object()

    assert stored_configuration.product_id == "mi"
    assert stored_configuration.device_id == "di"
    assert stored_configuration.device_status == DeviceStatus.PAIRED
    assert stored_configuration.bluetooth_enabled == True
    assert stored_configuration.aid == "aid"
    assert stored_configuration.public_key == "puk"
    assert stored_configuration.private_key == "prk"

    value = Storage.has_configuration()

    assert value

    Storage.remove_configuration()
