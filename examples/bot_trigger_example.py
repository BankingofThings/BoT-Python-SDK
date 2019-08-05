import time
import bot_python_sdk.bot_api_service as BotSDK
import json
from bot_python_sdk.logger import Logger

Component = 'BoT_Application'


if __name__ == "__main__":
    makerid = ''
    multipairingS = 'no'
    aid = 0
    BotSDKHndl = BotSDK.BoTApiService(makerid, multipairingS, aid)
    #print("Bot Handle Created ")
    Logger.info(Component, 'Bot Handle Created')
#    try:
#        BotSDKHndl.start()
#        #print("BotSDK API service started successfully ....")
#        Logger.info(BoT_Application, 'BotSDK API service started successfully ....')
#    except BotSDKHndl.BoTinputError as Error:
#        #print('Error from BoT API Service : '+Error.msg)
#        Logger.error(BoT_Application, Error.msg)

    # PSOT Triggers
    actionRes = BotSDK.ActionsResource()
    response = actionRes.get_actions()
    #print('GET Action Response : ' + json.dumps(response))
    Logger.info(Component, 'GET Action Response : ' + json.dumps(response))
    
    # GET Pairing details
    pairingRes = BotSDK.PairingResource()
    try:
      response = pairingRes.get_pairing_status()
      #print('GET Pairing Response : ' + json.dumps(response))
      Logger.info(Component, 'GET Pairing Response : ' + json.dumps(response))
    except BotSDK.DeviceForbiddenError as Error:
      #print('Error from BoT API Service : '+Error.msg)
      Logger.error(Component, Error.msg)
      
    # '{"actionID":"YOUR_ACTION_ID"}'
    triggerData = {"actionID":"4D047330-0066-4778-BEA9-DDC49A644583"}
    #triggerData = {"actionID":"4D047330-0066-4778-BEA9-DDC49A644583","alternativeID":"123456"}
    
    try:
       response = actionRes.trigger_actions(triggerData)
       #print('GET Action Response : ' + json.dumps(response))
       Logger.info(Component, 'Actions Response : ' + json.dumps(response))
    except BotSDK.DeviceForbiddenError as Error:
      #print('Error from BoT API Service : '+Error.msg)
      Logger.error(Component, Error.msg)
    except BotSDK.InvalidRequestError as Error:
      #print('Error from BoT API Service : '+Error.msg)
      Logger.error(Component, Error.msg)
    except BotSDK.ServiceUnavailableError as Error:
      #print('Error from BoT API Service : '+Error.msg)
      Logger.error(Component, Error.msg)
    
        
    time.sleep(10)
    
    
    