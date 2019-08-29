#!/usr/bin/env python3
# All offline requests/reposnses are processed in this module. Creates the thread for
# processing the trigger request which were to be processed when the device is online.
# During offline the trigger request are captured via linux inotify events and stored
# in the internal queues. Once the device is online, the Actions Processing thread reads
# the trigger events one after the other and processes it.
import threading
import time
import queue
import json
import glob
import shutil
import os
import socket
import pyinotify

from bot_python_sdk.logger import Logger
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.action_service import ActionService

## Remote server to connect to check internet availablity
REMOTE_SERVER_NAME = "www.google.com"
## all actions which are not processed (np) are stored in this location
_actions_np_db_file_path = 'storage/actions/np/'
## all processed actions are copied here.
## !Warning: Need to figure out what to do next with these files. Should we discard it ?
_actions_processed_db_file_path = 'storage/actions/processed/'

## JSON extension of all the offline actions data file
_actions_file_ext = 'json'

LOCATION = 'TriggerHandler'

## Actions processing thread wait time
MAX_WAIT_ACTION_PROCESSOR_TIME_IN_MS = 0.1 # 100 ms sleep time for thread
ACTION_PROCESSING_THREAD_ID = 0x0001

## Actions processing thread class
class ActionProcessing(threading.Thread):

    """Actions Processing class, responsible for process all offline actions once online.
    """
    def __init__(self, athObject, threadID, name):
      """The constructor. Stores the necessay objects """
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.ath = athObject
      #print (name)

    ## Starts the actions processing thread.
    #  @param : self, action processing object pointer.
    def run(self):
        Logger.info(LOCATION, "{} Action Processing Thread Started Successfully !".format(self.getName()))
        while(self.ath.bApplicationRunning):
            # Check the network and internet availability
            if (self.ath.isInternetAvailable(REMOTE_SERVER_NAME)):
                #if internet available, then process the requests
                while( (self.ath.actionsQ.qsize() > 0) ):
                    #aResource = ActionsResource()
                    # get the actions form the Queue and trigger the actions
                    req = self.ath.actionsQ.get()
                    value = req['value']
                    action_id = req['actionID']
                    alternative_id = req['alternativeID']
                    queue_id = req['queueID']
                    #Logger.info(LOCATION, 'Trigger Data :')
                    #Logger.info(LOCATION, '------------------------------------------')
                    #Logger.info(LOCATION, str(value))
                    #Logger.info(LOCATION, '------------------------------------------')

                    if (self.ath.actionservice.trigger(action_id, value, alternative_id,queue_id) == True):
                        Logger.info(LOCATION, 'Triggered Req Successfully !')
                    else:
                        Logger.error(LOCATION, 'Trigger Req Failed !')
                # Queue is empty then read from file and fill it
                # make sure nothing is pending to be processed from that specific location
                # !Warning : As of now not sure if this block is needed as inotify events
                # make sure the files are processed and data is copied to queue
                if (self.ath.actionsQ.qsize() == 0):
                   global _actions_np_db_file_path
                   actions_files_types = _actions_np_db_file_path + '*.json'
                   actions_to_prcoess_list = glob.glob(actions_files_types)
                   #print(actions_to_prcoess_list)
                   while actions_to_prcoess_list:
                      current_actions_np_file = actions_to_prcoess_list.pop(0)
                      #try:
                      with open(current_actions_np_file, 'r') as jsonfile:
                           req_dict = json.load(jsonfile)
                           self.ath.actionsQ.put(req_dict)
                           #print(_actions_processed_db_file_path)
                           shutil.move(current_actions_np_file, _actions_processed_db_file_path)
                      #except:
                      #  Logger.error(LOCATION, 'Invalid Action Trigger File Found')
                      #  break
            #if nothing to process then wait for sime time
            time.sleep(MAX_WAIT_ACTION_PROCESSOR_TIME_IN_MS)
        Logger.info(LOCATION, "{} Action Processing Thread Exited Successfully !".format(self.getName()))

## PyInotify file events class, defines necessary events to be processed
class BOTFileEventHandler(pyinotify.ProcessEvent):

    _methods = ["IN_CREATE", "IN_CLOSE_WRITE"]

    def __init__(self, athObject):
        pyinotify.ProcessEvent.__init__(self)
        self.ath = athObject

## Action Trigger handler class, interface to higher layers to trigger actions
class ActionTriggerHandler():

    """Actions Trigger handler class, responsible for configuring the offline mode and creating necessary
       resources needed to store/process the offline triggered actions data.
    """
    def __init__(self):
        """The constructor. Stores the necessay objects """
        self.configuration = ConfigurationStore().get()
        self.actionservice = ActionService()
        self.key_generator = KeyGenerator()
        self.action_processor = ActionProcessing(self, ACTION_PROCESSING_THREAD_ID, "ActionProcessingThread")

        self.bApplicationRunning = False
        #pass

    def initialize(self):
        """Creates/initializes the data structures and queues """
        self.bApplicationRunning = True
        ## Actions Queue
        self.actionsQ = queue.Queue()
        #pass

    def start(self):
        """ Starts the action processor thread and initializes the inotifier thread loop """
        self.action_processor.start()
        #Setup Inotify
        self.setupNotifier()

    def stop(self):
        """ Stop the necessary thread and stop the inotify loop """
        self.bApplicationRunning = False
        self.eventnotifier.stop()

        # wait untill the thread is closed successfully
        self.action_processor.join()

    def get_timestamp_millisec(self):
        """ create the timestamp in millisec """
        milliseconds = int(round(time.time() * 1000))
        return milliseconds

    def register_inotify_methods(self, cls, method):
      def _method_name(self, event):
        """ Event handler to process the PyInotify file envents """
        Logger.info(LOCATION, "Method name: {}()\n"
               "Path name: {}\n"
               "Event Name: {}\n".format(method, event.pathname, event.maskname))
        current_actions_np_file = event.pathname
        if ( (method == 'IN_CREATE') or (method == 'IN_CLOSE_WRITE')):
            with open(current_actions_np_file, 'r') as jsonfile:
                req_dict = json.load(jsonfile)
                # reads the json object from the file and puts it onto the Queue
                self.ath.actionsQ.put(req_dict)
                #print(_actions_processed_db_file_path)
                shutil.move(current_actions_np_file, _actions_processed_db_file_path)

      """ registers the inotify events to be observed """
      _method_name.__name__ = "process_{}".format(method)
      setattr(cls, _method_name.__name__, _method_name)

    def setupNotifier(self):
        """ setup necessary variables to enable thread based inotify events processing """
        self.watchMgr = pyinotify.WatchManager()
        #self.eventnotifier = pyinotify.Notifier(self.watchMgr, BOTFileEventHandler())
        self.eventnotifier = pyinotify.ThreadedNotifier(self.watchMgr, BOTFileEventHandler(self))

        self.to_watch = os.path.abspath(_actions_np_db_file_path)
        for method in BOTFileEventHandler._methods:
          Logger.info(LOCATION, "Registering Event Handler : {}".format(method))
          self.register_inotify_methods(BOTFileEventHandler,method)
        self.watchMgr.add_watch(self.to_watch, pyinotify.ALL_EVENTS)
        self.eventnotifier.start()

    @staticmethod
    def isInternetAvailable(hostname):
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(hostname)
            # connect to the host -- tells us if the host is actually
            # reachable
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
             pass
        return False

    def createReq(self,actionID=None, alternativeID=None, multipair=False, value=None):
        """ Creates the request JSON object """
        '''
          {
             "offlineAction":"true",
             "deviceID":,
             "makerID":"",
             "actionID":"",
             "queueID":"",
             "multipair":"false",
             "alternativeID":"",
             "value":"",
             "timestamp":"",
          }
        '''
        current_ts = self.get_timestamp_millisec()
        req_dict = {
             "offlineAction":"true",
             "deviceID":self.configuration.get_device_id(),
             "makerID":self.configuration.get_maker_id(),
             "actionID":actionID,
             "queueID":self.key_generator.generate_uuid(),
             "multipair":multipair,
             "alternativeID":alternativeID,
             "value":value,
             "timestamp":current_ts
            }
        #req_json = json.dumps(req_dict)
        return req_dict

    def store(self, req_dict):
        """ Stores the actions request json object @ _actions_np_db_file_path location """
        global _actions_np_db_file_path
        # create the json file @ /tmp folder and then copy that to store/actions/np/ folder
        # this would enable PyInotify events to be triggered and processed properly
        temp_actions_files = '/tmp/'+ 'actions_' + str(req_dict['timestamp']) + '.' + _actions_file_ext
        # Store the req to persistance database (DB/FILE)
        #current_actions_np_file = _actions_np_db_file_path + 'actions_' + str(req_dict['timestamp']) + '.' + _actions_file_ext
        try:
          #with open(current_actions_np_file, 'w') as jsonfile:
          with open(temp_actions_files, 'w') as jsonfile:
            json.dump(req_dict, jsonfile)
            shutil.move(temp_actions_files, _actions_np_db_file_path)
          return True
        except:
            pass
        return False

    def parseReq(self, req):
        # parse the json req whcih was saved and process it
        return[reqToProcess, reqObject]
