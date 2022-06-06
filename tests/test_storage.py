from cryptography.fernet import Fernet

from bot_python_sdk.data.configuration import Configuration
from bot_python_sdk.data.storage import Storage
from bot_python_sdk.util.key_generator import KeyGenerator


def test_has_no_configuration():
    Storage.remove_configuration()
    value = Storage.has_configuration()

    assert not value


def test_has_configuration():
    configuration = Configuration()
    configuration.initialize("mi", "di", True, True, "aid", "puk")

    Storage.save_configuration_object(configuration)

    stored_configuration = Storage.get_configuration_object()

    assert stored_configuration.get_product_id() == "mi"
    assert stored_configuration.get_device_id() == "di"
    assert stored_configuration.get_is_multi_pair()
    assert stored_configuration.get_is_bluetooth_enabled()
    assert stored_configuration.get_alternative_id() == "aid"
    assert stored_configuration.get_public_key() == "puk"

    value = Storage.has_configuration()

    assert value

    Storage.remove_configuration()


def test_private_key_storage():
    Storage.store_aes_key(Fernet.generate_key())
    public_key, private_key = KeyGenerator.generate_key()
    Storage.store_private_key(private_key)
    restored_pkey = Storage.get_private_key()

    assert private_key == restored_pkey
