import RPi.GPIO as GPIO          
import time

IN1L = 27
IN2L = 22
ENAL = 17

IN1R = 10
IN2R = 9
ENAR = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1L, GPIO.OUT)
GPIO.setup(IN2L, GPIO.OUT)
GPIO.setup(ENAL, GPIO.OUT)

GPIO.setup(IN1R, GPIO.OUT)
GPIO.setup(IN2R, GPIO.OUT)
GPIO.setup(ENAR, GPIO.OUT)

# Create a PWM object for controlling the motor speed
pwm_L = GPIO.PWM(ENAL, 1000)
pwm_R = GPIO.PWM(ENAR, 1000)

# Start the PWM with a duty cycle of 50%
pwm_L.start(80)
pwm_R.start(80)

# Set the motor direction (clockwise or counterclockwise)
GPIO.output(IN1L, GPIO.HIGH)
GPIO.output(IN2L, GPIO.LOW)

GPIO.output(IN1R, GPIO.HIGH)
GPIO.output(IN2R, GPIO.LOW)

# Wait for 5 seconds
time.sleep(5)

# Stop the motor
GPIO.output(IN1L, GPIO.LOW)
GPIO.output(IN2L, GPIO.LOW)
GPIO.output(IN1R, GPIO.HIGH)
GPIO.output(IN2R, GPIO.LOW)

# Cleanup the GPIO pins
GPIO.cleanup()