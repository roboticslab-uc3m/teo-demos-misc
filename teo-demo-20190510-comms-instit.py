#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CopyPolicy: released under the terms of the LGPLv2.1
# URL: https://github.com/roboticslab-uc3m/

robot = '/teoSim'

from time import sleep

# YARP
import yarp  # imports YARP
yarp.Network.init()  # connect to YARP network
if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print('[error] Please try running yarp server')  # tell the user to start one with 'yarp server' if there isn't any
    quit()

#-- Left Arm (LA)
optionsLA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsLA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsLA.put('remote',robot+'/leftArm')  # we add info on to whom we will connect
optionsLA.put('local','/demo'+robot+'/leftArm')  # we add info on how we will call ourselves on the YARP network
ddLA = yarp.PolyDriver(optionsLA)  # create a YARP multi-use driver with the given options
posLA = ddLA.viewIPositionControl()  # make a position controller object we call 'pos'
axesLA = posLA.getAxes()  # retrieve number of joints

#-- Right Arm (RA)
optionsRA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRA.put('remote',robot+'/rightArm')  # we add info on to whom we will connect
optionsRA.put('local','/demo'+robot+'/rightArm')  # we add info on how we will call ourselves on the YARP network
ddRA = yarp.PolyDriver(optionsRA)  # create a YARP multi-use driver with the given options
posRA = ddRA.viewIPositionControl()  # make a position controller object we call 'pos'
axesRA = posRA.getAxes()  # retrieve number of joints

#-- HEAD (H)
optionsH = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsH.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsH.put('remote',robot+'/head')  # we add info on to whom we will connect
optionsH.put('local','/demo'+robot+'/head')  # we add info on how we will call ourselves on the YARP network
ddH = yarp.PolyDriver(optionsH)  # create a YARP multi-use driver with the given options
posH = ddH.viewIPositionControl()  # make a position controller object we call 'pos'
axesH = posH.getAxes()  # retrieve number of joints

#-- Right Thumb (RT)
optionsRT = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRT.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRT.put('remote',robot+'/rightThumb')  # we add info on to whom we will connect
optionsRT.put('local','/demo'+robot+'/rightThumb')  # we add info on how we will call ourselves on the YARP network
ddRT = yarp.PolyDriver(optionsRT)  # create a YARP multi-use driver with the given options
posRT = ddRT.viewIPositionControl()  # make a position controller object we call 'pos'
axesRT = posRT.getAxes()  # retrieve number of joints

#-- Right Index (RI)
optionsRI = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRI.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRI.put('remote',robot+'/rightIndex')  # we add info on to whom we will connect
optionsRI.put('local','/demo'+robot+'/rightIndex')  # we add info on how we will call ourselves on the YARP network
ddRI = yarp.PolyDriver(optionsRI)  # create a YARP multi-use driver with the given options
posRI = ddRI.viewIPositionControl()  # make a position controller object we call 'pos'
axesRI = posRI.getAxes()  # retrieve number of joints

#-- Right Middle (RM)
optionsRM = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRM.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRM.put('remote',robot+'/rightMiddle')  # we add info on to whom we will connect
optionsRM.put('local','/demo'+robot+'/rightMiddle')  # we add info on how we will call ourselves on the YARP network
ddRM = yarp.PolyDriver(optionsRM)  # create a YARP multi-use driver with the given options
posRM = ddRM.viewIPositionControl()  # make a position controller object we call 'pos'
axesRM = posRM.getAxes()  # retrieve number of joints

#-- Right Ring (RR)
optionsRR = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRR.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRR.put('remote',robot+'/rightRing')  # we add info on to whom we will connect
optionsRR.put('local','/demo'+robot+'/rightRing')  # we add info on how we will call ourselves on the YARP network
ddRR = yarp.PolyDriver(optionsRR)  # create a YARP multi-use driver with the given options
posRR = ddRR.viewIPositionControl()  # make a position controller object we call 'pos'
axesRR = posRR.getAxes()  # retrieve number of joints

#-- Right Pinky (RP)
optionsRP = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRP.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRP.put('remote',robot+'/rightPinky')  # we add info on to whom we will connect
optionsRP.put('local','/demo'+robot+'/rightPinky')  # we add info on how we will call ourselves on the YARP network
ddRP = yarp.PolyDriver(optionsRP)  # create a YARP multi-use driver with the given options
posRP = ddRP.viewIPositionControl()  # make a position controller object we call 'pos'
axesRP = posRP.getAxes()  # retrieve number of joints

#-- Text-to-speech (TTS)
tts = yarp.RpcClient()
tts.open('/demo/espeak/rpc:c')
yarp.Network.connect('/demo/espeak/rpc:c','/espeak/rpc:s');

def ttsLang(language):
    cmd = yarp.Bottle()
    res = yarp.Bottle()
    cmd.addString('setLanguage')
    cmd.addString(language)
    tts.write(cmd,res)

def ttsSay(sayStr):
    cmd = yarp.Bottle()
    res = yarp.Bottle()
    cmd.addString('say')
    cmd.addString(sayStr)
    tts.write(cmd,res)

def ttsSpeed(speed):
    cmd = yarp.Bottle()
    res = yarp.Bottle()
    cmd.addString('setSpeed')
    cmd.addDouble(speed)
    tts.write(cmd,res)

#-- Pause rutine
import sys, tty, termios
def pause():
    print('in pause...')
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

#-- Program
# Single joint would be: posLA.positionMove(0,-35)

def zero():
    print('zero: begin')
    v = yarp.DVector(axesRA,0.0)
    posRA.positionMove(v)
    while not posRA.checkMotionDone():
        sleep(0.1)
    print('zero: end')

def safe():
    print('safe: begin')
    v = yarp.DVector(axesRA,0.0)
    v[0]=-35
    v[3]=-35
    posRA.positionMove(v)
    while not posRA.checkMotionDone():
        sleep(0.1)
    print('safe: end')

def hello():
    print('hello: begin')
    v = yarp.DVector(axesRA,0.0)
    v[0]=-65
    v[3]=-85
    v[4]=85
    posRA.positionMove(v)
    while not posRA.checkMotionDone():
        sleep(0.1)

    v[2]=10
    posRA.positionMove(v)
    while not posRA.checkMotionDone():
        sleep(0.1)

    v[2]=-10
    posRA.positionMove(v)
    while not posRA.checkMotionDone():
        sleep(0.1)

    v[2]=0
    posRA.positionMove(v)
    while not posRA.checkMotionDone():
        sleep(0.1)
    print('hello: end')

### INIT
zero()
safe()
hello()
safe()
zero()

quit()

ttsSpeed(160)

ttsLang('mb-es1')

ttsSay('¡Hola! Soy un robot asistencial que está aprendiendo a hablar lengua de signos y que asiste a la comunidad académica e investigadora en la difusión de los avances de los robots de mi naturaleza.')
sleep(0.5)

ttsSay('Mi nombre es TEO, en referencia a Operador en el Entorno de las Tareas. Me encargo de todas aqueyas labores que puedan hacer la vida más cómoda y liberar tiempo del día a día a mis compañeros humanos en el hogar. Puedo planchar, doblar ropa, servir comida y hasta me he aventurado a pintar en estos últimos años.')
sleep(0.5)

ttsSay('Aprender distintas formas de comunicación es fundamental de cara a una integración más efectiva de los robots en la sociedad. Por este motivo estoy aprendiendo, además, la Lengua de Signos Española con ayuda del equipo de Robotics Lab.')
sleep(0.2)
ttsSay('¿Sabías que en España alrededor de 13 mil trescientas personas emplean la lengua de signos para comunicarse?')
ttsSay('¡Por eso decidimos ponernos manos a la obra!')
sleep(0.5)

ttsSay('Para un robot, aprender lengua de signos es un proceso de lo más interesante.')
v = yarp.DVector(axesRA,0.0)
v[0]=-45
v[3]=-45
posRA.positionMove(v)
ttsSay('Implica inteligencia artificial, redes neuronales, visión artificial y unas increíbles manos robóticas sub-actuadas.')
sleep(1)

ttsSay(' El proceso que sigue mi equipo para enseñarme a signar se puede resumir del siguiente modo:')
sleep(0.2)
ttsSay('En primer lugar, un ser humano instructor me indica, a través de una simulación, cómo colocar las falanges de mis dedos para representar determinados signos.')
sleep(0.2)
ttsSay('En segundo lugar, se tiene en cuenta que mis falanges no funcionan exactamente igual que las humanas para idear una adaptación de los movimientos a mi mano. El objetivo es que queden parecidos y, sobre todo, naturales. Se prueban varios tipos de redes neuronales para que modelen esta adaptación y, así, elegir aqueya que logre hacer los gestos de forma comprensible para las personas que se comunican con la lengua de signos.')
sleep(0.2)
ttsSay('Por último, la colaboración de individuos sordos es fundamental para aceptar o rechazar un modelo de lengua de signos representado. Esta última fase es lo que, en el laboratorio, yamamos fase de validación. ¡Los avances en la ciencia se construyen entre todos!')
sleep(0.5)

ttsSay('¡Los resultados obtenidos mediante estas técnicas han sido prometedores! Los signos generados mediante estas técnicas han producido en torno a un 80% de respuestas positivas de reconocimiento de signos entre los participantes en la fase de validación. Es decir: cuatro de cada cinco veces, los usuarios entendían lo que quería decirles.')
sleep(0.2)

ttsSay('Mi deseo es que en un futuro próximo pueda contribuir a facilitar ciertos aspectos tediosos de la vida cotidiana a todas las personas que lo necesiten o lo deseen. Para ello, seguimos y seguiremos trabajando con vehemencia tanto en aspectos de interacción humano-robot, como en la mejora y ampliación de las tareas que soy capaz de desarroyar. Sin más que agregar, me despido con una de las frases que más me inspiran en mi proceso de aprendizaje y mejora: Hay una sola luz en la ciencia y, alumbrarla en cualquier lugar, es alumbrarla en todos los lugares.')

