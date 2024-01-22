import time
import numpy as np
from utils import plot_line
from Motor_ENC import Motor

# Assigning parameter values
T = 2  # Period of sine wave (s)
u0 = 1  # Motor output amplitude
tstop = 2  # Sine wave duration (s)
tsample = 0.01  # Sampling period for code execution (s)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
# Integrated encoder is on GPIO pins 25 and 25
mymotor = Motor(
    enable1=17, pwm1=27, pwm2=22,
    encoder1=25, encoder2=8, encoderppr=300.8)
mymotor.reset_angle()

# Pre-allocating output arrays
t = []
theta = []

# Initializing current time step and starting clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running motor sine wave output
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Assigning motor sinusoidal output using the current time step
    mymotor.set_output(u0 * np.sin((2*np.pi/T) * tcurr))
    # Updating output arrays
    t.append(tcurr)
    theta.append(mymotor.get_angle())
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor

# Calculating motor angular velocity (rpm)
w = 60/360 * np.gradient(theta, t)

# Plotting results
plot_line([t, t, t[1::]], [theta, w, 1000*np.diff(t)], axes='multi',
          yname=[
              'Angular Position (deg.)',
              'Angular velocity (rpm)',
              'Sampling Period (ms)'])