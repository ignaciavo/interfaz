from werkzeug.wrappers import response
from app import app
from flask import render_template, request, redirect
import serial
import time

from scipy import signal

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot


s = serial.Serial(port='/dev/ttyS1', baudrate=9600, timeout=.1)


#cu.usbserial-1410
#cu.usbserial-A50285BI

@app.route('/', methods=['GET','POST'])
def home():

    url=None
    ciclo=66
    frecuencia=request.form.get('frecuencia')
    voltaje=48 
    vs=None
    pr=0
    ccp_= None

    if request.method == "POST":
        print('Frecuencia-----> {}'.format(request.form.get('frecuencia')))
        ciclo=request.form.get('ciclo')
        frecuencia=request.form.get('frecuencia')
        voltaje=request.form.get('voltaje')
        
        s.write('30'.encode())
        time.sleep(0.05)
        s.write('pr'.encode())
        time.sleep(0.05)
        s.write('31'.encode())
        time.sleep(0.05)
        s.write('ccp_'.encode())
        time.sleep(0.05)
       

        url=grafico(ciclo,frecuencia)
        vs=voltaje_salida(ciclo,voltaje)
        pr=PR2(ciclo,frecuencia)
        ccp_= CCP1(ciclo,frecuencia)

        print(ciclo, frecuencia, voltaje)

       #return redirect(request.url)

    return render_template('home.html', url=url, ciclo=ciclo, frecuencia=frecuencia, voltaje=voltaje, vs=vs)

def grafico(c,f):
    plot.figure().clear()
    plot.close()
    plot.cla()
    plot.clf()

    # Sampling rate 1000 hz / second
    t = np.linspace(0, 1, 1000, endpoint=True)
    # Plot the square wave signal
    plot.plot(t, 2.5+2.5*signal.square(2 * np.pi * round(float(f),2) * t, duty = round(float(c),2)/100))
    # Give x axis label for the square wave plot
    plot.xlabel('Time')
    # Give y axis label for the square wave plot
    plot.ylabel('Amplitude')
    plot.grid(True, which='both')
    # Provide x axis and line color
    plot.axhline(y=0, color='k')
    # Set the max and min values for y axis
    plot.ylim(-1, 6)
    # Display the square wave drawn
    plot.savefig('app/static/img/square.png')
    #plot.show()
    return 'app/static/img/square.png'
      

def voltaje_salida(c,v):
    return round(float(c),2)*round(float(v))/100

def PR2 (c,f):
    fosc=48000000
    pr2=round((fosc/(float(f))*4*4)-1)
    pr2=chr(pr2)
    return pr2

def CCP1(c,f):
    fosc=48000000
    ccpr1l=round(((float(c)/100)*fosc)/(4*float(f)))
    print(ccpr1l)
    return ccpr1l












