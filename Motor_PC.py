import time
import numpy as np
from gpiozero_extended import Motor,PID

# Setting general parameters
tstop = 5  # Execution duration (s)
tsample = 0.01  # Sampling period (s)
thetamax = 180  # Motor position amplitude (deg)

# Setting motion parameters
# (Valid options: 'sin', 'cos')
option = 'cos'
if option == 'sin':
    T = 2*tstop  # Period of sine wave (s)
    theta0 = thetamax  # Reference angle
elif option == 'cos':
    T = tstop  # Period of cosine wave (s)
    theta0 = 0.5*thetamax  # Reference angle

# Creating PID controller object
kp = 0.036
ki = 0.379
kd = 0.0009
taupid = 0.01
pid = PID(tsample, kp, ki, kd, tau=taupid)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
# Integrated encoder on GPIO pins 24 and 25.
mymotor = Motor(
    enable1=17, pwm1=27, pwm2=22,
    encoder1=25, encoder2=8, encoderppr=300.8)
mymotor.reset_angle()

# Initializing variables and starting clock
thetaprev = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Getting motor shaft angular position
    thetacurr = mymotor.get_angle()
    # Calculating current set point angle
    if option == 'sin':
        thetaspcurr = theta0 * np.sin((2*np.pi/T) * tcurr)
    elif option == 'cos':
        thetaspcurr = theta0 * (1-np.cos((2*np.pi/T) * tcurr))
    # Calculating closed-loop output
    ucurr = pid.control(thetaspcurr, thetacurr)
    print(ucurr)
    # Assigning motor output
    mymotor.set_output(ucurr)
    # Updating previous values
    thetaprev = thetacurr
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor