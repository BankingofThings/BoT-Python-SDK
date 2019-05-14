from enum import Enum


class DeviceStatus(Enum):
    NEW = 'NEW'
    PAIRED = 'PAIRED'
    ACTIVE = 'ACTIVE'
    MULTIPAIR = 'MULTIPAIR'

