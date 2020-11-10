from bot_python_sdk.configuration import Configuration
from bot_python_sdk.device_status import DeviceStatus
from unittest import mock
import pytest


@pytest.fixture()
def resource():
    resource = mock.Mock()
    resource.product_id = 'product id'
    resource.device_id = 'device id'
    resource.device_status = DeviceStatus.MULTIPAIR
    resource.bluetooth_enabled = True
    resource.aid = 'aid'
    resource.public_key = ''
    resource.private_key = ''
    return resource


def test_configuration():
    configuration = Configuration()
    assert not configuration.is_initialized()


def test_configuration_initialize(resource):
    configuration = _initialize(resource)
    assert configuration.is_initialized()


def test_get_headers(resource):
    configuration = _initialize(resource)

    header = {
        'Content-Type': 'application/json',
        'makerID': resource.product_id,
        'deviceID': resource.device_id
    }

    assert configuration.get_headers() == header


def test_get_device_information(resource):
    configuration = _initialize(resource)

    device_info = {
        'deviceID': resource.device_id,
        'makerID': resource.product_id,
        'publicKey': resource.public_key,
        'multipair': 1,
        'aid': resource.aid
    }

    assert configuration.get_device_information() == device_info


def _initialize(resource):
    configuration = Configuration()
    configuration.initialize(
        resource.product_id,
        resource.device_id,
        resource.device_status,
        resource.bluetooth_enabled,
        resource.aid,
        resource.public_key,
        resource.private_key
    )
    return configuration
