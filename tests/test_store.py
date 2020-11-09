from bot_python_sdk.configuration import Configuration
from bot_python_sdk.store import Store


def test_has_no_configuration():
    value = Store.has_configuration()

    assert not value


def test_has_configuration():
    configuration = Configuration()

    Store.create_windows_folder()

    Store.save_configuration_object(configuration)

    value = Store.has_configuration()

    assert value


def test_save_configuration_object():
    configuration = Configuration()

    Store.save_configuration_object(configuration)

    Store.has_configuration()
