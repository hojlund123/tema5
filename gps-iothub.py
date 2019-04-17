from gps3 import agps3
from time import sleep
import csv
import datetime
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import time
import os
os.system('sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock')
CONNECTION_STRING = "HostName=tema5gps........."
PROTOCOL = IoTHubTransportProvider.MQTT
MSG_TXT = "{\"latitude\": %.6f,\"longitude\": %.6f,\"speedy\": %.6f}"""
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()
fname = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%y-%H-%M-%S')
filename = "%s.csv" % fname

def send_confirmation_callback(message, result, user_context):
    print ( "Response: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                if data_stream.lat == "n/a":
                    print("Ingen GPS signal")
                    break
                else:
                    latitude = float(data_stream.lat)
                    longitude = float(data_stream.lon)
                    speedy = float(data_stream.speed) * 3.6
                    msg_txt_formatted = MSG_TXT % (latitude, longitude, speedy)
                    
                mydate = datetime.datetime.now()
                csvstr = datetime.datetime.strftime(mydate, '%d/%m-%Y %H:%M:%S')
                if data_stream.speed == "n/a":
                    speedy = data_stream.speed
                else:
                    speedy = float(data_stream.speed) * 3.6
                client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
                message = IoTHubMessage(msg_txt_formatted)
                client.send_event_async(message, send_confirmation_callback, None)
                print(csvstr+": IoT Hub: "+msg_txt_formatted)
                #gemmer csvfil med titel csvstr
                with open(filename, "a") as csv_file:
                	csv_app = csv.writer(csv_file)
                	csv_app.writerow([csvstr, data_stream.lat, data_stream.lon, speedy])
                time.sleep(1)
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
