from weioLib.weio import *

def setup() :
    attach.process(blinky)

def blinky() :
    print "Hello world!"
    pause = 100
    while True:
        digitalWrite(20, HIGH)
        delay(pause)
        digitalWrite(20, LOW)
        delay(pause)
