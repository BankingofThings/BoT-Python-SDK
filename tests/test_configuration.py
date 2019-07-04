from bot_python_sdk.configuration import Configuration
from bot_python_sdk.device_status import DeviceStatus
from unittest import mock
import pytest

@pytest.fixture()
def resource():
	m = mock.Mock()
	m.maker_id = 'maker id'
	m.device_id = 'device id'
	m.device_status = DeviceStatus.MULTIPAIR.value
	m.aid = 'aid'
	m.public_key = ''
	m.private_key = ''
	return m
    
def test_configuration():
	configuration = Configuration()
	assert configuration.is_initialized() == False
	

def test_configuration_initialize(resource):
	
	configuration = Configuration()
	configuration.initialize(resource.maker_id, resource.device_id, resource.device_status,
					 resource.aid, resource.public_key, resource.private_key)
	assert configuration.is_initialized() == True

def test_get_headers(resource):
	
	configuration = Configuration()
	configuration.initialize(resource.maker_id, resource.device_id, resource.device_status,
					 resource.aid, resource.public_key, resource.private_key)

	header = {
		'Content-Type': 'application/json',
        'makerID': resource.maker_id,
        'deviceID': resource.device_id
	}

	assert configuration.get_headers() == header

def test_get_device_information(resource):

	configuration = Configuration()
	configuration.initialize(resource.maker_id, resource.device_id, resource.device_status,
					 resource.aid, resource.public_key, resource.private_key)

	device_info = {
            'deviceID': resource.device_id,
            'makerID': resource.maker_id,
            'publicKey': resource.public_key,
			'multipair': 1,
            'aid': resource.aid
		}

	assert configuration.get_device_information() == device_info







	