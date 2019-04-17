from gps3 import agps3
from time import sleep
import RPi.GPIO as GPIO
from dragino import Dragino
import os
import time
import datetime
GPIO.setwarnings(False)

#lora
D = Dragino("dragino.ini")
D.join()

#gps
os.system('sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock')
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()

while True:
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.lat == "n/a":
                print("Ingen GPS signal")
                time.sleep(1)
                break
            else:
                mydate = datetime.datetime.now()
                csvstr = datetime.datetime.strftime(mydate, '%d/%m-%Y %H:%M:%S')
                decimal_latitude = "{0:.7f}".format(data_stream.lat)
                decimal_longitude = "{0:.7f}".format(data_stream.lon)
                decimal_speed = (3.6*data_stream.speed)
                decimal_str = csvstr,decimal_latitude,decimal_longitude,decimal_speed
                print(decimal_str)
                D.send(decimal_str)
                print("Sendt til TTN")
                time.sleep(1)