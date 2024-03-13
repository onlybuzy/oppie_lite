
#importacion de librerias necesarias
import time
import numpy as np
from utils import plot_line
from gpiozero_extended import Motor, PID

# Parametros Generales
tstop = 2  # Tiempo de ejecucuion 
tsample = 0.01  # Tiempo de muestro
wsp = 12  # Set point inicial 
tau = 0.1  # Filtro de baja frecuencia

# PID
kp = 0.25
ki = 0.5
kd = 0.01
taupid = 0.01
pid = PID(tsample, kp, ki, kd, umin=0, tau=taupid)

mymotor_1 = Motor(
    enable1=17, pwm1=27, pwm2=22,
    encoder1=25, encoder2=8, encoderppr=300.8)

mymotor_1.reset_angle()



#Arrays para almacenar datos
t = []
w = []
wf = []
u = []

# Inicializacion
ucurr = 0  
wfprev = 0  
wfprev_2 = 0
wfcurr = 0  

thetaprev = 0
thetaprev_2 = 0
tprev = 0
tprev_2=0
tcurr = 0
tstart = time.perf_counter()

#Ciclo de trabajo

print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    #pausa durante el tiempo de muestreo para recolectar datos 
    time.sleep(tsample)
    tcurr = time.perf_counter() - tstart
    thetacurr = mymotor_1.get_angle()
    wcurr = np.pi/180 * (thetacurr-thetaprev)/(tcurr-tprev)
     #Filtro de velocidad de señal
     
    wfcurr = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr
    wfprev = wfcurr
    
    # Lazo cerrado
    ucurr = pid.control(wsp, wfcurr)
    # Se da velocidad al motor
    mymotor_1.set_output(ucurr)
    
    t.append(tcurr)
    w.append(wcurr)
    wf.append(wfcurr)
    u.append(ucurr)
    thetaprev = thetacurr
    tprev = tcurr
    tprev_2 = tcurr

print(tcurr)
tcurr=0


while tcurr <= tstop+2:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    tcurr = time.perf_counter() - tstart
    thetacurr = mymotor_1.get_angle()
    wcurr = np.pi/180 * (thetacurr-thetaprev)/(tcurr-tprev)
    wfcurr = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr
    wfcurr_2 = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr_2
    wfprev = wfcurr
    wfprev_2 = wfcurr_2
    ucurr = pid.control(8, wfcurr)
    ucurr_2 = pid.control(8, wfcurr_2)
    mymotor_1.set_output(ucurr)
    t.append(tcurr)
    w.append(wcurr)
    wf.append(wfcurr)
    u.append(ucurr)
    thetaprev = thetacurr
    tprev = tcurr
    tprev_2 = tcurr
    
while tcurr <= tstop+4:
    time.sleep(tsample)
    tcurr = time.perf_counter() - tstart
    thetacurr = mymotor_1.get_angle()
    wcurr = np.pi/180 * (thetacurr-thetaprev)/(tcurr-tprev)
    wfcurr = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr
    wfprev = wfcurr
    wfprev_2 = wfcurr_2
    ucurr = pid.control(8, wfcurr)
    mymotor_1.set_output(ucurr)
    print(wfcurr_2)
    t.append(tcurr)
    w.append(wcurr)
    wf.append(wfcurr)
    u.append(ucurr)
    thetaprev = thetacurr
    tprev = tcurr
    tprev_2 = tcurr

print('Done.')


mymotor_1.set_output(0, brake=True)

del mymotor_1



