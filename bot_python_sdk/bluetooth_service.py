from bot_python_sdk.logger import Logger
import time
from bluetooth import *

LOCATION = 'Bluetooth Service'
RESOURCE = 'ble'
UUID = '729BE9C4-3C61-4EFB-884F-B310B6FFFFD1'


class BluetoothService:
    
    def connection_establishment_server(self):
        server_sock=BluetoothSocket(RFCOMM)
        server_sock.bind(("12:ab:34:ad:ty",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = UUID

        advertise_service( server_sock, "Bluetooth Server",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ], 
        #                   protocols = [ OBEX_UUID ] 
                            )
                           
        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        try:
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0: break
                print("received [%s]" % data)
                returnResponse = {"response" : "success"}
        except IOError:
            returnResponse = {"response" : "failed"}
        
        print("disconnected")
        client_sock.close()
        server_sock.close()
        print("all done")
        return returnResponse
    
    
    
    
    
        


