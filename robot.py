import RPi.GPIO as GPIO   

import atexit



class motors_move:
    
    def __init__(self):
        self.PWMA = 17
        self.AIN1 = 27
        self.AIN2 = 22
        self.PWMB = 11
        self.BIN1 = 10
        self.BIN2 = 9
        
        atexit.register(self.stopMotors)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.PWMA, GPIO.OUT)

        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.PWMB, GPIO.OUT)
           
    
    def convert_speed(self,speed):
       
        pwm_L = GPIO.PWM(ENAL, 1000)
        pwm_R = GPIO.PWM(ENAR, 1000)  
       
        pwm_L.start(speed)
        pwm_R.start(speed)
        
        if speed >0:
            
            GPIO.output(IN1L, GPIO.HIGH)
            GPIO.output(IN2L, GPIO.LOW)

            GPIO.output(IN1R, GPIO.HIGH)
            GPIO.output(IN2R, GPIO.LOW)
        
        if speed <0:
            
             GPIO.output(IN1L, GPIO.LOW)
             GPIO.output(IN2L, GPIO.HIGH)

             GPIO.output(IN1R, GPIO.LOW)
             GPIO.output(IN2R, GPIO.HIGH)
        
        if speed==0:
            
             GPIO.output(IN1L, GPIO.LOW)
             GPIO.output(IN2L, GPIO.LOW)

             GPIO.output(IN1R, GPIO.LOW)
             GPIO.output(IN2R, GPIO.LOW)
    
            