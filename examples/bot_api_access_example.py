import time
import threading
import bot_python_sdk.bot_api_service as BotSDK
import json
from bot_python_sdk.logger import Logger

import signal
import sys

Component = 'BoT_Application'

bApplicationExit = 0
timeToSleep = 0.2 #200 ms sleep

def handleExitEvent(sig, frame):
        msg = 'User Pressed Ctrl+C! ...'
        Logger.error(Component, msg)
        global bApplicationExit
        bApplicationExit = 1
        #sys.exit(0)

#print('Press Ctrl+C')
#signal.pause()
signal.signal(signal.SIGINT, handleExitEvent)

'''  
def exitHanderThread():
    print("THREAD : Handle External Exit Event  ... ")
    global timeToSleep
    global bApplicationExit
    while(!bApplicationExit):
        time.sleep(timeToSleep) # sleep for 200 ms
    print("THREAD : Exiting the Application thread ... ")
'''    
if __name__ == "__main__":
    
    makerid = ''
    multipairingS = 'no'
    aid = 0

    if len (sys.argv) == 1:
       Logger.info(Component, 'Execute w/o Maker ID ')
    elif len (sys.argv) == 2:
       # Maker ID provided ..
       Logger.info(Component, 'Only Maker ID Provided ')
       makerid = sys.argv[1]
    elif len (sys.argv) < 4:
       msg = 'Please provide all the parameters as \'sudo python3 bot_example01.py <MakerID> <Multipairing Status as yes/no> <Alternate ID>'
       Logger.error(Component, msg)
       sys.exit(0)
    else:
       makerid = sys.argv[1]
       multipairingS = sys.argv[2]
       aid = sys.argv[3]

    
    print(makerid)
    print(multipairingS)
    print(aid)
    
    #sys.exit(0)
    BotSDKHndl = BotSDK.BoTApiService(makerid, multipairingS,aid)
    #print("Bot Handle Created ")
    Logger.info(Component, 'Bot Handle Created')
    # creating thread 
    #tAppExit = threading.Thread(target=exitHanderThread)
    
    try:
        BotSDKHndl.start()
        #print("BotSDK API service started successfully ....")
        Logger.info(Component, 'BotSDK API service started successfully ....')
    except BotSDK.BoTinputError as Error:
        #print('Error from BoT API Service : '+Error.msg)
        Logger.error(Component, Error.msg)
        sys.exit(0)
    except BotSDK.MissingInputError as Error:
        Logger.error(Component, Error.msg)
        sys.exit(0)
        
    msg = 'To Exit the Test Appplication, Press Ctrl+C ...'
    Logger.info(Component, msg)
    
    while(bApplicationExit == 0):
        time.sleep(timeToSleep) # sleep for 200 ms
    msg = 'Application : Exiting the Application (Ctrl+C pressed) ...'    
    Logger.error(Component, msg)
    BotSDKHndl.start()
    
    time.sleep(0.5)
    sys.exit(0)

