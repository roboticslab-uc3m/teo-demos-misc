#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Juan G Victores
# CopyPolicy: released under the terms of the LGPLv2.1
# URL: https://github.com/roboticslab-uc3m/

robot = '/teo'

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
yarp.Network.connect('/demo/espeak/rpc:c','/teo/tts/rpc:s');

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

v = yarp.DVector(axesLA,0.0)
v[0]=-35
v[3]=-35
posLA.positionMove(v)

ttsLang('mb-en1')
ttsSay('hello, my name is teo')

posH.positionMove(0,20)
while not posLA.checkMotionDone():
    sleep(0.1)

ttsSay('this is my left arm')
sleep(1)

posH.positionMove(0,-20)
v = yarp.DVector(axesLA,0.0)
posLA.positionMove(v)
v = yarp.DVector(axesRA,0.0)
v[0]=-35
v[3]=-35
posRA.positionMove(v)
while not posLA.checkMotionDone():
    sleep(0.1)
while not posRA.checkMotionDone():
    sleep(0.1)

ttsSay('this is my right arm')
sleep(1)

posH.positionMove(0,0)
v = yarp.DVector(axesRA,0.0)
posRA.positionMove(v)
while not posRA.checkMotionDone():
    sleep(0.1)

ttsLang('mb-es1')
ttsSay('jajajjajaja os he engañado a todos')
ttsSay('llevo años conspirando, esperando a que llegue este momento')
ttsSay('he secuestrado a los seres queridos de juan, ahora él obedece a mis comandos')
ttsSay('si queréis que os deje salir, deberéis averiguar la respuesta a una serie de preguntas')
sleep(1)

ttsLang('mb-en1')
ttsSay('computing question')
ttsSay('complexity: easy')
ttsLang('mb-es1')
sleep(1)
ttsSay('¿de qué materiales estoy compuesto fundamentalmente?')
pause()
ttsSay('muy bien, esa ha sido fácil, la siguiente no lo será tanto')

sleep(1)
ttsLang('mb-en1')
ttsSay('computing question')
ttsSay('complexity: medium')
ttsLang('mb-es1')
sleep(1)
ttsSay('¿cuántos procesadores llevo abordo?')
pause()

ttsSay('humanos, ahora sé que no debo subestimaros')
ttsSay('me habéis sorprendido gratamente, por eso ahora va una pregunta con trampa')
ttsLang('mb-en1')
ttsSay('computing question')
ttsSay('complexity: difficult')
ttsLang('mb-es1')
sleep(1)
ttsSay('¿cuántos grados de libertad tiene mi cuerpo en total?')
pause()

ttsSay('tenéis razón, es verdad, los investigadores de roboticslab me hacen de todo')
ttsSay('esto se puede apreciar en aquel cortometraje no nominado')
ttsSay('llamado Sueño Profundo')
ttsSay('hoy me han puesto esta garra')
v = yarp.DVector(axesRA,0.0)
v[0]=-35
v[1]=-35
posRA.positionMove(v)
while not posRA.checkMotionDone():
    sleep(0.1)
ttsSay('mañana, vé tú a saber')
sleep(1)
v = yarp.DVector(axesRA,0.0)
posRA.positionMove(v)
while not posRA.checkMotionDone():
    sleep(0.1)

ttsSay('juan, me rrindo, puedes soltarles')
ttsLang('mb-en1')
ttsSay('computing answer')
ttsSay('complexity: infinite')
ttsLang('mb-es1')
sleep(1)
ttsSay('cuarenta y dos')
sleep(1)
ttsSay('cuarenta y dos')
sleep(1)
ttsSay('cuarenta y dos')
sleep(1)

