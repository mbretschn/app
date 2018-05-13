import redis
import RPi.GPIO as GPIO
import time
from rrdtool import update as rrd_update

GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    StopZeit = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
 
    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2
 
    return distanz
 

r = redis.StrictRedis(host="localhost", port=6379, db=0)

while True:
    value = distance()
    r.publish('distance', value)

    rrd_update('/home/pi/Development/data/distance.rrd', 'N:%s' % value)            

    time.sleep(1)
