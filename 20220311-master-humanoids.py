#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Juan G Victores
# CopyPolicy: released under the terms of the LGPLv2.1
# URL: https://github.com/roboticslab-uc3m/

import yarp
from yarp import DVector
import roboticslab_speech as speech
from time import sleep

robot = '/teoSim'

yarp.Network.init()

if not yarp.Network.checkNetwork():
    print('Please try running yarp server')
    raise SystemExit

#-- Left Arm (LA)

optionsLA = yarp.Property()
optionsLA.put('device', 'remote_controlboard')
optionsLA.put('remote', robot + '/leftArm')
optionsLA.put('local', '/demo' + robot + '/leftArm')
ddLA = yarp.PolyDriver(optionsLA)
posLA = ddLA.viewIPositionControl()

if not ddLA.isValid():
    print('Left arm device not available')
    raise SystemExit

#-- Right Arm (RA)

optionsRA = yarp.Property()
optionsRA.put('device', 'remote_controlboard')
optionsRA.put('remote', robot + '/rightArm')
optionsRA.put('local', '/demo' + robot + '/rightArm')
ddRA = yarp.PolyDriver(optionsRA)
posRA = ddRA.viewIPositionControl()

if not ddRA.isValid():
    print('Right arm device not available')
    raise SystemExit

#-- HEAD (H): head is dead, long live the head!

optionsH = yarp.Property()
optionsH.put('device', 'remote_controlboard')
optionsH.put('remote', robot + '/head')
optionsH.put('local', '/demo' + robot + '/head')
ddH = yarp.PolyDriver(optionsH)
posH = ddH.viewIPositionControl()

if not ddH.isValid():
    print('Head device not available')
    raise SystemExit

#-- Text-to-speech (TTS)

ttsRPC = yarp.RpcClient()

if not ttsRPC.open('/demo/tts/rpc:c'):
    print('Unable to open TTS client port %s' % ttsRPC.getName())
    raise SystemExit

if not yarp.Network.connect(ttsRPC.getName(), '/teo/tts/rpc:s'):
    print('Unable to connect to remote TTS server port')
    raise SystemExit

tts = speech.SpeechSynthesis()
tts.yarp().attachAsClient(ttsRPC)

#-- Utilities

def awaitKeypress():
    import sys, tty, termios
    print('in pause...')
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def sayAndWait(sentence):
    tts.say(sentence)

    while not tts.checkSayDone():
        sleep(0.1)

def awaitMotion(device):
    while not device.checkMotionDone():
        sleep(0.1)

#-- Program

tts.setLanguage('mb-en1')
sayAndWait('hello, my name is teo')
sleep(1.0)

posH.positionMove(0, 20.0)
posLA.positionMove(DVector([-35.0, 0.0, 0.0, -35.0, 0.0, 0.0]))
awaitMotion(posLA)

sayAndWait('this is my left arm')
sleep(1.0)

posH.positionMove(0, -20.0)
posLA.positionMove(DVector(6, 0.0))
posRA.positionMove(DVector([-35.0, 0.0, 0.0, -35.0, 0.0, 0.0]))

awaitMotion(posLA)
awaitMotion(posRA)

sayAndWait('this is my right arm')
sleep(1.0)

posH.positionMove(0, 0.0)
posRA.positionMove(DVector(6, 0.0))
awaitMotion(posRA)

tts.setLanguage('mb-es1')
sayAndWait('jajajjajaja os he engañado a todos')
sayAndWait('ievo años conspirando, esperando a que iegue este momento')
sayAndWait('he secuestrado a los seres queridos de juan, ahora él obedece a mis comandos')
sayAndWait('si queréis que os deje salir, deberéis averiguar la rrespuesta a una serie de preguntas')
sleep(1.0)

tts.setLanguage('mb-en1')
sayAndWait('computing question')
sayAndWait('complexity: easy')
tts.setLanguage('mb-es1')
sleep(1.0)
sayAndWait('de qué materiales estoy compuesto fundamentalmente?')
awaitKeypress()
sayAndWait('muy bien, esa ha sido fácil, la siguiente no lo será tanto')

sleep(1.0)
tts.setLanguage('mb-en1')
sayAndWait('computing question')
sayAndWait('complexity: medium')
tts.setLanguage('mb-es1')
sleep(1.0)
sayAndWait('cuántos procesadores ievo a bordo?')
awaitKeypress()

sayAndWait('humanos, ahora sé que no debo subestimaros')
sayAndWait('me habéis sorprendido gratamente, por eso ahora va una pregunta con trampa')
tts.setLanguage('mb-en1')
sayAndWait('computing question')
sayAndWait('complexity: difficult')
tts.setLanguage('mb-es1')
sleep(1.0)
sayAndWait('cuántos grados de libertad tiene mi cuerpo en total?')
awaitKeypress()

sayAndWait('tenéis rrazón, es verdad, los investigadores de rroboticslab me hacen de todo')
sayAndWait('esto se puede apreciar en aquel cortometraje no nominado')
sayAndWait('iamado Sueño Profundo')

posRA.positionMove(DVector([-35.0, 0.0, 0.0, -35.0, 0.0, 0.0]))
sayAndWait('hoy me han puesto esta gara')
awaitMotion(posRA)

sayAndWait('mañana, vete tú a saber')
sleep(1.0)

posRA.positionMove(DVector(6, 0.0))
awaitMotion(posRA)

sayAndWait('juan, me rrindo, puedes soltarles')

tts.setLanguage('mb-en1')
sayAndWait('computing answer')
sayAndWait('complexity: infinite')

tts.setLanguage('mb-es1')
sleep(1.0)
sayAndWait('cuarenta y dos')
sleep(1.0)
sayAndWait('cuarenta y dos')
sleep(1.0)
sayAndWait('cuarenta y dos')
sleep(1.0)
