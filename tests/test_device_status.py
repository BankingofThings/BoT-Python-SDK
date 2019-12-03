from bot_python_sdk.device_status import DeviceStatus


def test_device_status_length():
    assert len(DeviceStatus) == 4


def test_device_status_names():
    assert DeviceStatus.NEW.name == 'NEW'
    assert DeviceStatus.PAIRED.name == 'PAIRED'
    assert DeviceStatus.ACTIVE.name == 'ACTIVE'
    assert DeviceStatus.MULTIPAIR.name == 'MULTIPAIR'


def test_device_status_values():
    assert DeviceStatus.NEW.value == 'NEW'
    assert DeviceStatus.PAIRED.value == 'PAIRED'
    assert DeviceStatus.ACTIVE.value == 'ACTIVE'
    assert DeviceStatus.MULTIPAIR.value == 'MULTIPAIR'
