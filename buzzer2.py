# coding: utf-8
import RPi.GPIO as GPIO
import time

SOUNDER = 23
DOREMI_Hz = [ 262, 294, 330, 349, 392, 440, 494, 523 ]

GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUNDER, GPIO.OUT, initial = GPIO.LOW)

p = GPIO.PWM(SOUNDER, 1)
p.start(50)

for Hz in DOREMI_Hz :
    p.ChangeFrequency(Hz)
    time.sleep(1)

p.stop()
GPIO.cleanup()