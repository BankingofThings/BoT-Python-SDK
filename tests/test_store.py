from bot_python_sdk.configuration import Configuration
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.store import Store


def test_has_no_configuration():
    value = Store.has_configuration()

    assert not value


def test_has_configuration():
    configuration = Configuration()
    configuration.initialize("mi","di",DeviceStatus.ACTIVE, True, "aid", "puk", "prk")

    Store.save_configuration_object(configuration)

    stored_configuration = Store.get_configuration_object()

    assert stored_configuration.product_id == "mi"
    assert stored_configuration.device_id == "di"
    assert stored_configuration.device_status == DeviceStatus.ACTIVE
    assert stored_configuration.bluetooth_enabled == True
    assert stored_configuration.aid == "aid"
    assert stored_configuration.public_key == "puk"
    assert stored_configuration.private_key == "prk"

    value = Store.has_configuration()

    assert value

    Store.remove_configuration()
