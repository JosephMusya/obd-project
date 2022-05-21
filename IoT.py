import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import I2C_LCD

disp = I2C_LCD.lcd()
Red = 14
Green = 15
Blue = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)

GPIO.output(Red, False)
GPIO.output(Green, False)
GPIO.output(Blue, False)

iot_hub = "demo.thingsboard.io"
port = 1883
username = "adUqGERkNURBtutPXfNs"
password = ""
topic = "v1/devices/me/telemetry"

def connect(): 
    try:
        disp.lcd_clear()
        disp.lcd_display_string("Connecting...", 2)
        GPIO.output(Red, True)
        time.sleep(0.5)

        GPIO.output(Red, False)
        GPIO.output(Blue, True)
        time.sleep(0.5)

        GPIO.output(Blue, False)
        client = mqtt.Client()
        client.username_pw_set(username,password)
        a = client.connect(iot_hub,port)
        if a is 0:
            disp.lcd_clear()
            disp.lcd_display_string("Connected...", 1, 2)
            time.sleep(.5)
        return client
    except:
        disp.lcd_clear()
        disp.lcd_display_string("--No Internet--",2)
        disp.lcd_display_string("Not Connected!!!",1)
        time.sleep(3)
        disp.lcd_clear()
        disp.lcd_display_string("Reconnecting...")
        time.sleep(3)
        connect()

if __name__ == "__main__":
    connect()
    
    
    
    
    
    
    
    

