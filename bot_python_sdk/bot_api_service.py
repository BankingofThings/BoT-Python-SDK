"""@package docstring
BOT API service module provides interface for applications to interact with BOT Services.
Applications have to import the module and create object of the BotApiService class.
Then call the corresponding API's and classes to interface with BOT Service
"""
import os
import sys
import json
from bot_python_sdk.store import Store
from bot_python_sdk.action_service import ActionService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger

from bot_python_sdk.bluetooth_service import BluetoothService

## Global variables to interface with BOT Services.
LOCATION = 'Controller'
INCOMING_REQUEST = 'Incoming request: '

DEVICE_ID_KEY = 'deviceId'
MAKER_ID_KEY = 'makerId'
PUBLIC_KEY_KEY = 'publicKey'

ACTION_ID = 'actionID'
VALUE_KEY = 'value'
ALTERNATIVER_ID ='alternativeID'

METHOD_GET = 'get'
METHOD_POST = 'set'
ACTIONS_ENDPOINT = 'actions'
PAIRING_ENDPOINT = 'pairing'
ACTIVATION_ENDPOINT = 'activation'

class BoTerror(Exception):

    """BoT API service Exception class, using which all the exceptions are created.
    """
    pass

class DeviceForbiddenError(BoTerror):

    """BoT API service Device Forbidden Exception. This shall be triggered when
       the device status is not active
    """
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class InvalidRequestError(BoTerror):

    """BoT API service Invalid Request Exception. This shall be triggered when
       the actionID or alternateID is missing from the action trigger request.
    """
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class ServiceUnavailableError(BoTerror):

    """BoT API service Service Not Available Exception. This shall be triggered when
       the triggered action request is failed from the BOT service.
    """
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class BoTinputError(BoTerror):
    
    """BoT API service no imput provided Exception. This shall be triggered when
       a new device pairing is requested with out maker id being provided.
    """
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class MissingInputError(BoTerror):

    """BoT API service Missing Input Exception. This shall be triggered when
       either multipairing is enabled and alternative ID is 0 or invalid.
    """
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class NetworkUnavailableError(BoTerror):
    
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class ActionsTriggerStoreError(BoTerror):
    
    def __init__(self, error):
        """The constructor. Stores the error message which the application can access """
        self.msg = error

class ActionsResource:
    
    """ Action Resource class is responsible for interfacing with Action Service and
        either get the actions requested or trigger the actions.
    """
    def __init__(self):
        """ Constructor. Initializes/creates the action service and configuration store objects"""
        """@var action_service : stores action service object"""
        """@var configuration_store : stores configuration store object"""
        self.action_service = ActionService()
        self.configuration_store = ConfigurationStore()

    ## Gets the list of actions from the action service/makerid server.
    #  @param self The object pointer.
    def get_actions(self):
        Logger.info(LOCATION, INCOMING_REQUEST + METHOD_GET + ' ' + ACTIONS_ENDPOINT)
        response = self.action_service.get_actions()
        return response

    ## Triggers the actions.
    #  @param self The object pointer.
    #  @param actions_to_set actions to perform (dictionary).
    def trigger_actions(self, actions_to_set):
        configuration = self.configuration_store.get()
        device_status = configuration.get_device_status()

        # if device status is not active/multipair, then its an ivalid state to trigger action.
        if device_status is not DeviceStatus.ACTIVE and device_status is not DeviceStatus.MULTIPAIR:
            error = 'Not allowed to trigger actions when device is not activated.'
            Logger.error(LOCATION, error)
            raise DeviceForbiddenError(error)

        Logger.info(LOCATION, INCOMING_REQUEST + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
        data = actions_to_set

        #If actionID is missing then throw an error
        if ACTION_ID not in data.keys():
            Logger.error(LOCATION, 'Missing parameter `' + ACTION_ID + '` for ' + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
            raise InvalidRequestError('Missing parameter')

        if device_status is DeviceStatus.MULTIPAIR:
            if ALTERNATIVER_ID not in data.keys():
                Logger.error(LOCATION, 'Missing parameter `' + ALTERNATIVER_ID + '` for ' + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
                raise InvalidRequestError('Missing parameter alternativeID')

        action_id = data[ACTION_ID]
        value = data[VALUE_KEY] if VALUE_KEY in data.keys() else None
        alternative_id = data[ALTERNATIVER_ID] if ALTERNATIVER_ID in data.keys() else None

        success = self.action_service.trigger(action_id, value, alternative_id)
        response = ''
        if success:
            response = {'message': 'Action triggered'}
            return response
        else:
            error = 'action service trigger failed, service not available'
            raise ServiceUnavailableError(error)


class PairingResource:
    
    """ Pairing Resource class is responsible for interfacing with Pairing Service to
        get the pairing status of the device with the FINN application. 
    """
    def __init__(self):
        """ Constructor. Initializes/creates the configuration store and configuration service objects"""
        """@var configuration_service : stores configuration service object"""
        """@var configuration_store : stores configuration store object"""
        self.configuration_store = ConfigurationStore()
        self.configuration_service = ConfigurationService()

    def get_pairing_status(self):
        Logger.info(LOCATION, INCOMING_REQUEST + METHOD_GET + ' ' + PAIRING_ENDPOINT)
        configuration = self.configuration_store.get()
        if configuration.get_device_status() is not DeviceStatus.NEW:
            error = 'Device is already paired.'
            Logger.error(LOCATION, error)
            raise DeviceForbiddenError(error)
        device_information = configuration.get_device_information()
        response = json.dumps(device_information)
        #subprocess.Popen(['make', 'pair'])
        self.configuration_service.pair()
        return response


class ActivationResource:
    
    def __init__(self):
        self.configuration_service = ConfigurationService()

    def activate_service(self):
        self.configuration_service.resume_configuration()

class BoTApiService():
    
    """ BOT API Service class provides interfaces for BOT SDK. Applications can
        import this class and call the api's to talk to BOT service
    """
    def __init__(self, makerid, multipairing='no', aid=0):
        ## Constructor
        self.makerID = makerid
        self.multipairStatus = multipairing
        self.aid = aid

    def start(self):
        configuration_service = ConfigurationService()
        store = Store()

        if( (self.multipairStatus == 'yes') and (self.aid == 0)):
           raise MissingInputError('Alternate ID is missing')

        if not store.has_configuration():
            if (self.makerID == ''): # if no maker ID then raise an exception
                error = 'Maker ID missing to configure the SDK'
                raise BoTinputError(error)
            #Module based or Server based. 0:Module based
            configuration_service.initialize_configuration(self.makerID, 0, self.multipairStatus, self.aid)

        #Initialize the Bluetooth service class to process BLE specific events and callbacks
        BluetoothService().initialize()
        configuration_service.resume_configuration()