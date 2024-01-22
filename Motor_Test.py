import time
import numpy as np
from Motor import Motor 

# Assigning parameter values
T = 4  # Period of sine wave (s)
u0 = 1  # Motor output amplitude
tstop = 4  # Sine wave duration (s)
tsample = 0.01  # Sampling period for code execution (s)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
mymotor = Motor(enable1=16, pwm1=17, pwm2=18)

# Initializing current time stamp and starting clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running motor sine wave output
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Doing I/O every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Assigning motor sinusoidal output using the current time stamp
        mymotor.set_output(u0 * np.sin((2*np.pi/T) * tcurr))
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor