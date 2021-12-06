#! /usr/bin/env python

from werkzeug.wrappers import response
from app import app         #inicializamos la direccion web en este archivo
from flask import render_template, request, redirect
import serial               #Pyserial para las conexiones seriales
import time                 #para implementar retrasos o time.sleep()
from scipy import signal    
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot

s = serial.Serial(port='COM6', baudrate=9600, parity= serial.PARITY_NONE,stopbits= serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)


@app.route('/', methods=['GET','POST'])
def home():

    url=None
    ciclo=66
    frecuencia=20000
    voltaje=30 
    vs=None
    pr=None
    ccp_= None
    ccp_2=None


    if request.method == "POST":
        
        ciclo=request.form.get('ciclo')
        frecuencia=request.form.get('frecuencia')
        voltaje=request.form.get('voltaje')
        print('Frecuencia-----> {}'.format(request.form.get('frecuencia')))

        url=grafico(ciclo,frecuencia)
        vs=voltaje_salida(ciclo)
        pr=PR2(ciclo,frecuencia)
        ccp_= CCP1CON(ciclo,frecuencia)
        ccp_2=CCPR1L(ciclo,frecuencia)
        cicl=ciclo1(voltaje)

        pr=chr(pr)
        s.write(pr.encode())
        print(pr)
        time.sleep(0.3)

        ccp_2=chr(ccp_2)
        s.write(ccp_2.encode())
        print(ccp_2)
        time.sleep(0.3)

        ccp_=chr(ccp_)
        s.write(ccp_.encode())
        print(ccp_)
        time.sleep(0.3)
       
    #return redirect(request.url)

        return render_template('home.html', url=url, ciclo=ciclo, frecuencia=frecuencia, voltaje=voltaje, vs=vs,s=s,cicl=cicl)



def grafico(c,f):
    plot.figure().clear()
    plot.close()
    plot.cla()
    plot.clf()

    # Sampling rate 1000 hz / second
    t = np.linspace(0, 1, 1000, endpoint=True)
    # Plot the square wave signal
    plot.plot(t, 2.5+2.5*signal.square(2 * np.pi * round(float(f),2) * t, duty = round(float(c),2)/100))
    plot.xlabel('Time')
    plot.ylabel('Amplitude')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.ylim(-1, 6)
    # Display the square wave drawn
    plot.savefig('app/static/img/square.png')   #guarda el gráfico en esa dirección de la carpeta de la interfaz
    return 'app/static/img/square.png'
      

def voltaje_salida(c):
    return round(float(c),2)*round(float(48))/100

def ciclo1(v):
    return round(float(v))/round(float(48))*100

def PR2 (c,f):
    fosc=48000000
    #f sobre 3k
    pr2=round((fosc/((float(f))*16*4))-1)
    return pr2

def CCP1CON(c,f):
    fosc=48000000
    ccpr1l=round(((float(c)/100)*fosc)/(16*float(f))) 
    ccpcon=(ccpr1l & 0x003) << 4
    ccpcon=(ccpcon|0x0C)
    return ccpcon

def CCPR1L(c,f):
    fosc=48000000
    ccpr1l=round(((float(c)/100)*fosc)/(16*float(f)))
    ccpr1l=ccpr1l >> 2
    return ccpr1l
