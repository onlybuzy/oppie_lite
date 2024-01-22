import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define the motor pins
IN1 = 17
IN2 = 27
ENA = 22

# Set the motor pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Create a PWM object for controlling the motor speed
pwm = GPIO.PWM(ENA, 1000)

# Start the PWM with a duty cycle of 50%
pwm.start(50)

# Set the motor direction (clockwise or counterclockwise)
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

# Wait for 5 seconds
time.sleep(5)

# Stop the motor
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)

# Cleanup the GPIO pins
GPIO.cleanup()