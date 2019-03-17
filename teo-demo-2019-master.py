#!/usr/bin/env python

# Authors: Juan G Victores
# CopyPolicy: released under the terms of the LGPLv2.1
# URL: https://github.com/roboticslab-uc3m/

robot = '/teoSim'

from time import sleep

import yarp  # imports YARP
yarp.Network.init()  # connect to YARP network
if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print '[error] Please try running yarp server'  # tell the user to start one with 'yarp server' if there isn't any
    quit()

optionsLA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsLA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsLA.put('remote',robot+'/leftArm')  # we add info on to whom we will connect
optionsLA.put('local','/demo'+robot+'/leftArm')  # we add info on how we will call ourselves on the YARP network
ddLA = yarp.PolyDriver(optionsLA)  # create a YARP multi-use driver with the given options

posLA = ddLA.viewIPositionControl()  # make a position controller object we call 'pos'
modeLA = ddLA.viewIControlMode2()  # make a operation mode controller object we call 'mode'

axesLA = posLA.getAxes()  # retrieve number of joints

# use the object to set the device to position mode (as opposed to velocity mode)(note: stops the robot)
modeLA.setControlModes(yarp.IVector(axesLA, yarp.encode('pos')))

posLA.positionMove(0,-35)
while not posLA.checkMotionDone():
    sleep(0.1)

posLA.positionMove(0,0)
while not posLA.checkMotionDone():
    sleep(0.1)

#min = yarp.DVector(1)

