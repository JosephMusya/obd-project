import IoT
import I2C_LCD
import gps
#import OBD

import random as r
import json
import time
import RPi.GPIO as GPIO
from time import *
from time import sleep
import requests

prev_z = 0
count = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

data,data1,data2,data3,data4,data5,data6, data7,data8 = dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict()

topic = IoT.topic
client = IoT.connect()
disp = I2C_LCD.lcd()

icon = [
            [0b00001,0b00001,0b00011,0b00011,0b00111,0b00111,0b01111,0b01111]
    ]

while True:
    scroll_f = GPIO.input(8)
    scroll_b = GPIO.input(11)
    check_dtc = GPIO.input(9)
    
    lat,lng = gps.get_loc()

    print("lat", lat, "long", lng)
    
    x = r.randint(30,37) #temp
    y = r.randint(95, 100) #rpm
    z = r.randint(85, 90) #fuel %
    a = r.randint(60, 67) #engine load %
    b = r.randint(70, 80) #speed

    data["Temperature"] = x
    data1["Engine RPM"] = y
    data2["Fuel Level"] = z
    data3["Engine Load"] = a
    data4["Speed"] = b
    data5["lat"] = lat
    data6["lng"] = lng

    data_out =  json.dumps( data)
    data1_out = json.dumps(data1)
    data2_out = json.dumps(data2)
    data3_out = json.dumps(data3)
    data4_out = json.dumps(data4)
    data5_out = json.dumps(data5)
    data6_out = json.dumps(data6)
    
    client.publish(topic,data_out, 0)
    client.publish(topic,data1_out,0)
    client.publish(topic,data2_out,0)
    client.publish(topic,data3_out,0)
    client.publish(topic,data4_out,0)
    client.publish(topic,data5_out,0)
    client.publish(topic,data6_out,0)
    
    z_len = len(str(z))
    if z_len < prev_z:
        disp.lcd_clear()
    if scroll_f == False:
        count = count + 1
        if count > 4:
            count = 1
        disp.lcd_clear()
    if scroll_b == False:
        count = count - 1
        disp.lcd_clear()
        if count < 1:
            count = 4
    if check_dtc == False:
        pass 
    if count == 1:
        disp.lcd_load_custom_chars(icon)
        disp.lcd_write(0x8f) #0x80 >>home
        disp.lcd_write_char(0)
        disp.lcd_display_string("Eng Temp:", 1)
        disp.lcd_display_string(str(x),1,10)
    elif count == 2:
        disp.lcd_display_string("Fuel Level:", 1)
        disp.lcd_display_string(str(z),1,12)
    elif count == 3:
        disp.lcd_display_string("Eng Load:", 1)
        disp.lcd_display_string(str(a),1,11)
    elif count == 4:
        disp.lcd_display_string("Speed:", 1)
        disp.lcd_display_string(str(b),1,8)
    sleep(.5)
  
    prev_z = z_len