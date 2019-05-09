#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Juan G Victores
# CopyPolicy: released under the terms of the LGPLv2.1
# URL: https://github.com/roboticslab-uc3m/

robot = '/teoSim'

from time import sleep

# YARP
import yarp  # imports YARP
yarp.Network.init()  # connect to YARP network
if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print '[error] Please try running yarp server'  # tell the user to start one with 'yarp server' if there isn't any
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

ttsLang('mb-es1')

ttsSay('Soy un robot asistencial que está aprendiendo a hablar lengua de signos y que asiste a la comunidad académica e investigadora en la difusión de los avances de los robots de mi naturaleza.')
sleep(0.5)

#ttsSay('Mi nombre es TEO, no como aquel entrañable personaje pelirrojo de los libros infantiles, sino en referencia a')
#ttsLang('mb-en1')
#ttsSay('Task Environment Operator')
#ttsLang('mb-es1')
#ttsSay('o, en casteyano, Operador en el Entorno de las Tareas.')
#sleep(0.2)
#ttsSay('Aunque, TEO, es mi nombre de pila, algunos investigadores prefieren yamarme R H 2, en referencia a la posición que ocupo en la estirpe de humanoides que surgió con mi abuelo, R H 0, hace ya quince años.')
#sleep(0.2)
#ttsSay('La vida del robot humanoide medio no es larga. El ritmo de los avances científicos y tecnológicos nos mantienen en constante transformación en la Universidad Carlos tercero de Madrid.')
#sleep(0.5)
#
#ttsSay('Es comprensible que te preguntes qué tipo de tareas yeva a cabo un humanoide como yo o a qué entorno hace referencia mi nombre. ¡Senciyo! Me encargo de todas aqueyas labores que puedan hacer la vida más cómoda y liberar tiempo del día a día a mis compañeros humanos en el hogar. Puedo planchar, doblar ropa, servir comida, y hasta me he aventurado a pintar en estos últimos años.')
#sleep(0.2)
#ttsSay('Aprender distintas formas de comunicación es fundamental de cara a una integración más efectiva de los robots en la sociedad. Por este motivo estoy aprendiendo, además, la Lengua de Signos Española (LSE) con ayuda de los científicos de Robotics Lab.')
#sleep(0.2)
ttsSay('¿Sabías que en España alrededor de 13 mil trescientas personas emplean la lengua de signos para comunicarse? Dado que las cifras estadísticas del INE apuntan a que en nuestro país impera una media de 2,5 personas por hogar')
ttsSay('-estos estadistas y su tendencia a partir a las personas por la mitad-')
ttsSay('conocer esta lengua me acerca a prestar ayuda a más de 5000 familias. ¡Por eso decidimos ponernos manos a la obra!')
sleep(0.5)

ttsSay('No es fácil imaginar cómo puede un robot aprender lengua de signos. Es un proceso de lo más interesante que envuelve inteligencia artificial, redes neuronales, visión artificial y unas increíbles manos robóticas sub-actuadas.')
v = yarp.DVector(axesLA,0.0)
v[0]=-35
v[3]=-35
posLA.positionMove(v)
sleep(0.5)

ttsSay('El proceso que sigue mi equipo para enseñarme a signar se puede resumir del siguiente modo:')
sleep(0.2)
ttsSay('En primer lugar, un ser humano instructor me indica, a través de una simulación, cómo colocar las falanges de mis dedos para representar determinados signos. El tiempo que se invierte en esta fase de mi aprendizaje es bastante extenso, pero merece la pena. ¡Nunca olvido lo que aprendo!')
sleep(0.2)
ttsSay('En segundo lugar, se tiene en cuenta que mis falanges no funcionan exactamente igual que las humanas para idear una adaptación de los movimientos a mi mano robótica. El objetivo es que queden parecidos y, sobre todo, naturales. Se prueban varios tipos de redes neuronales para que modelen esta adaptación y, así, elegir aqueya que logre hacer los gestos de forma comprensible para las personas que se comunican con la lengua de signos.')
sleep(0.2)
ttsSay('Por último, la colaboración de individuos sordos es fundamental para aceptar o rechazar un modelo de lengua de signos representado. Esta última fase es lo que, en el laboratorio, yamamos fase de validación. ¡Los avances en la ciencia se construyen entre todos!')


pause()

