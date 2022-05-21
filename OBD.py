import obd
import random as r
import time
import os

#f = open(r"/home/pi/DTC.txt")
#new_f = open(r"/home/pi/DTC.txt", encoding = 'utf-8')

connection = obd.Async()

rpm, speed, runtime, load = 0, 0, 0, 0

def rpm(r):
    global rpm
    rpm = int(r.value.magnitude)
def speed(s):
    global speed
    speed = int(s.value.magnitude)
def runtime(rn):
    global runtime
    runtime = int(rn.value.magnitude)
def load(l):
    global load
    load = int(l.value.magnitude)
def fuel(f):
    global fuel
    fuel = int(f.value.magnitude)
def mil(m):
    global mil
    mil = int(m.value.magnitude)
def check_dtc():
    obd.commands.GET_DTC()
    
connection.watch(obd.commands[1][12], callback = rpm) #PID value for rpm
connection.watch(obd.commands[1][13], callback = speed) #PID value for speed
connection.watch(obd.commands[1][31], callback = runtime) #Engine Runtime
connection.watch(obd.commands[1][4],  callback = load) #engine load
connection.watch(obd.commands[1][47], callback = fuel)
connection.watch(obd.commands[1][77], callback = mil)
connection.start() 

if __name__ == "__main":
    pass