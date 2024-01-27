
# Importing modules and classes
import time
import numpy as np
from utils import plot_line
from gpiozero_extended import Motor, PID

# Setting general parameters
tstop = 2  # Execution duration (s)
tsample = 0.01  # Sampling period (s)
wsp = 12  # Motor speed set point (rad/s)
tau = 0.1  # Speed low-pass filter response time (s)

# Creating PID controller object
kp = 0.25
ki = 0.5
kd = 0.01
taupid = 0.01
pid = PID(tsample, kp, ki, kd, umin=0, tau=taupid)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
# Integrated encoder on GPIO pins 24 and 25.
mymotor_1 = Motor(
    enable1=17, pwm1=27, pwm2=22,
    encoder1=25, encoder2=8, encoderppr=300.8)
mymotor_1.reset_angle()

mymotor_2 = Motor(
    enable1=11, pwm1=10, pwm2=9,
    encoder1=23, encoder2=24, encoderppr=300.8)

mymotor_2.reset_angle()

# Pre-allocating output arrays
t = []
w = []
wf = []
u = []

# Initializing previous and current values
ucurr = 0  # x[n] (step input)
wfprev = 0  # y[n-1]
wfprev_2 = 0
wfcurr = 0  # y[n]

# Initializing variables and starting clock
thetaprev = 0
thetaprev_2 = 0
tprev = 0
tprev_2=0
tcurr = 0
tstart = time.perf_counter()

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Getting motor shaft angular position: I/O (data in)
    thetacurr = mymotor_1.get_angle()
    thetacurr_2 = mymotor_2.get_angle()
    # Calculating motor speed (rad/s)
    wcurr = np.pi/180 * (thetacurr-thetaprev)/(tcurr-tprev)
    wcurr_2 = np.pi/180 * (thetacurr_2-thetaprev_2)/(tcurr-tprev_2)
    # Filtering motor speed signal
    wfcurr = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr
    wfcurr_2 = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr_2
    wfprev = wfcurr
    wfprev_2 = wfcurr_2
    # Calculating closed-loop output
    ucurr = pid.control(wsp, wfcurr)
    ucurr_2 = pid.control(wsp, wfcurr_2)
    # Assigning motor output: I/O (data out)
    mymotor_1.set_output(ucurr)
    print(wfcurr_2)
    mymotor_2.set_output(ucurr_2)
    # Updating output arrays
    t.append(tcurr)
    w.append(wcurr)
    wf.append(wfcurr)
    u.append(ucurr)
    # Updating previous values
    thetaprev = thetacurr
    thetaprev_2 = thetacurr_2
    tprev = tcurr
    tprev_2 = tcurr

print("Reversa")
tcurr=0

while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Getting motor shaft angular position: I/O (data in)
    thetacurr = mymotor_1.get_angle()
    thetacurr_2 = mymotor_2.get_angle()
    # Calculating motor speed (rad/s)
    wcurr = np.pi/180 * (thetacurr-thetaprev)/(tcurr-tprev)
    wcurr_2 = np.pi/180 * (thetacurr_2-thetaprev_2)/(tcurr-tprev_2)
    # Filtering motor speed signal
    wfcurr = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr
    wfcurr_2 = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr_2
    wfprev = wfcurr
    wfprev_2 = wfcurr_2
    # Calculating closed-loop output
    ucurr = pid.control(-wsp, wfcurr)
    ucurr_2 = pid.control(-wsp, wfcurr_2)
    # Assigning motor output: I/O (data out)
    mymotor_1.set_output(ucurr)
    print(wfcurr_2)
    mymotor_2.set_output(ucurr_2)
    # Updating output arrays
    t.append(tcurr)
    w.append(wcurr)
    wf.append(wfcurr)
    u.append(ucurr)
    # Updating previous values
    thetaprev = thetacurr
    thetaprev_2 = thetacurr_2
    tprev = tcurr
    tprev_2 = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor_1.set_output(0, brake=True)
mymotor_2.set_output(0,brake=True)
del mymotor_1
del mymotor_2



