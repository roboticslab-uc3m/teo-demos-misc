#! /usr/bin/env python

import sys
import yarp

homeLA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
homeRA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
homeLH = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
homeRH = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

helloRA1 = [-56.0, 9.9, 21.8, -99.6, 33.5, -26.1]
helloRA2 = [-59.6, 9.9, 21.8, -83.6, 33.5, -17.6]

myLA = [-24.5, 13.9, -51.6, -72.3, 0.0, 0.0]
myRA = [-55.0, -5.0, 57.0, -99.6, -56.5, 6.7]

nameLA = [-35.0, 7.0, -35.0, -85.0, 0.0, 0.0]
nameRA1 = [-65.0, 0.0, 50.0, -99.6, -20.0, 6.7]
nameRA2 = [-51.0, 2.0, 50.0, -80.0, -30.0, 15.0]
nameLH = [40.0, 2.0, 0.0, 0.0, 18.0, 18.0] # [40, 2, 0, 0, 20, 20]
nameRH = [40.0, 2.0, 0.0, 0.0, 18.0, 18.0] # [40, 2, 0, 0, 20, 20]

letterTA = [-73.2, 10.7, 10.6, -74.6, 34.7, 1.9]
letterTH = [57.3, 5.4, 14.9, 4.7, 1.5, 0.0]

letterEA = [-75.4, 12.4, 9.6, -83.5, 86.2, 2.3]
letterEH = [0.0, 0.0, 18.0, 18.0, 18.0, 18.0] # [0, 0, 20, 20, 20, 20]

letterOA = [-73.4, 10.5, 13.1, -83.5, 25.7, -0.9]
letterOH = [47.3, 1.9, 11.6, 5.0, 2.4, 0.0] # [87.3, 1.9, 11.6, 5.0, 2.4, 0.0]

def wait(*arg):
    for part in arg:
        while not part['pos'].checkMotionDone():
            pass

def moveTo(part, target, duration = 0.0):
    if not 'name' in part:
        return 
    
    if duration > 0.0:
        curr = yarp.DVector(6)
        part['enc'].getEncoders(curr)
        
        spds = yarp.DVector(6)
        part['pos'].getRefSpeeds(spds)
        
        maxSpeed = 0.0

        for j in range(6):
            spds[j] = abs(target[j] - curr[j]) / duration
            maxSpeed = max(maxSpeed, spds[j])
        
        print('(%s) new refSpeeds: %s (max: %f)' % (part['name'], ' '.join(map(str, spds)), maxSpeed))
        part['pos'].setRefSpeeds(spds)
    
    part['pos'].positionMove(yarp.DVector(target))

def say(text):
    global tts
    cmd = yarp.Bottle('say "%s"' % text)
    res = yarp.Bottle()
    tts.write(cmd, res)

if len(sys.argv) < 2:
    print('error: missing prefix parameter')
    quit()

robotPrefix = sys.argv[1]
demoPrefix = '/lsedemo' + robotPrefix

if robotPrefix == '/teo':
    isReal = True
elif robotPrefix == '/teoSim':
    isReal = False
else:
    print('error: illegal prefix parameter, choose "/teo" or "/teoSim"')
    quit()

yarp.Network.init()

if not yarp.Network.checkNetwork():
    print('error: please try running yarp server')
    quit()

tts = yarp.RpcClient()
tts.open(demoPrefix + '/tts/rpc:c')
yarp.Network.connect(tts.getName(), '/tts/rpc:s')

options = yarp.Property()
options.put('device', 'remote_controlboard')

options.put('remote', robotPrefix + '/leftArm')
options.put('local', demoPrefix + '/leftArm')
leftArmDevice = yarp.PolyDriver(options)
leftArmPos = leftArmDevice.viewIPositionControl()
leftArmEnc = leftArmDevice.viewIEncoders()

options.put('remote', robotPrefix + '/rightArm')
options.put('local', demoPrefix + '/rightArm')
rightArmDevice = yarp.PolyDriver(options)
rightArmPos = rightArmDevice.viewIPositionControl()
rightArmEnc = rightArmDevice.viewIEncoders()

LEFT_ARM = { 'name': 'leftArm', 'pos': leftArmPos, 'enc': leftArmEnc }
RIGHT_ARM = { 'name': 'rightArm', 'pos': rightArmPos, 'enc': rightArmEnc }
LEFT_HAND = {}
RIGHT_HAND = {}

if isReal:
    options.put('remote', robotPrefix + '/leftHand')
    options.put('local', demoPrefix + '/leftHand')
    leftHandDevice = yarp.PolyDriver(options)
    leftHandPos = leftHandDevice.viewIPositionControl()
    
    options.put('remote', robotPrefix + '/rightHand')
    options.put('local', demoPrefix + '/rightHand')
    rightHandDevice = yarp.PolyDriver(options)
    rightHandPos = rightHandDevice.viewIPositionControl()
    
    LEFT_HAND = { 'name': 'leftHand', 'pos': leftHandPos }
    RIGHT_HAND = { 'name': 'rightHand', 'pos': rightHandPos }

initialLeftArmRefSpeeds = yarp.DVector(6)
initialRightArmRefSpeeds = yarp.DVector(6)

leftArmPos.getRefSpeeds(initialLeftArmRefSpeeds)
rightArmPos.getRefSpeeds(initialLeftArmRefSpeeds)

print('initial left arm refSpeeds: %s' % ' '.join(map(str, initialLeftArmRefSpeeds)))
print('initial right arm refSpeeds: %s' % ' '.join(map(str, initialRightArmRefSpeeds)))

# home
print('*** Home ***')
moveTo(LEFT_ARM, homeLA)
moveTo(RIGHT_ARM, homeRA)
moveTo(LEFT_HAND, homeLH)
moveTo(RIGHT_HAND, homeRH)
wait(LEFT_ARM, RIGHT_ARM)

# hi
print('*** Hi ***')
moveTo(RIGHT_ARM, helloRA1, 4)
wait(RIGHT_ARM)
say('hola')
moveTo(RIGHT_ARM, helloRA2, 0.75)
wait(RIGHT_ARM)

yarp.delay(0.5)

# my
print('*** My ***')
moveTo(LEFT_ARM, myLA, 2)
moveTo(RIGHT_ARM, myRA, 2)
wait(LEFT_ARM, RIGHT_ARM)
say('mi')

yarp.delay(0.5)

# name
print('*** Name ***')
moveTo(LEFT_ARM, nameLA, 3)
moveTo(RIGHT_ARM, nameRA1, 1.25)
moveTo(LEFT_HAND, nameLH)
moveTo(RIGHT_HAND, nameRH)
wait(RIGHT_ARM)
say('nombre es')
moveTo(RIGHT_ARM, nameRA2, 1.75)
wait(LEFT_ARM, RIGHT_ARM)

yarp.delay(0.5)

# T
print('*** T ***')
moveTo(LEFT_ARM, myLA, 2.5)
moveTo(RIGHT_ARM, letterTA, 2.5)
moveTo(LEFT_HAND, homeLH)
moveTo(RIGHT_HAND, letterTH)
wait(LEFT_ARM, RIGHT_ARM)
say('T')

yarp.delay(0.5)

# E
print('*** E ***')
moveTo(RIGHT_ARM, letterEA, 2.5)
moveTo(RIGHT_HAND, letterEH)
wait(RIGHT_ARM)
say('E')

yarp.delay(0.5)

# O
print('*** O ***')
moveTo(RIGHT_ARM, letterOA, 2.5)
moveTo(RIGHT_HAND, letterOH)
wait(RIGHT_ARM)
say('O')

yarp.delay(0.5)
say('TEO')
yarp.delay(0.5)

# home
print('*** Home ***')
moveTo(LEFT_ARM, homeLA, 5)
moveTo(RIGHT_ARM, homeRA, 5)
moveTo(RIGHT_HAND, homeRH)
wait(LEFT_ARM, RIGHT_ARM)

leftArmPos.setRefSpeeds(initialLeftArmRefSpeeds)
rightArmPos.setRefSpeeds(initialLeftArmRefSpeeds)

leftArmDevice.close()
rightArmDevice.close()

if isReal:
    leftHandDevice.close()
    rightHandDevice.close()

tts.close()

yarp.Network.fini()
