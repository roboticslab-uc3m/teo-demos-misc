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

options = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
options.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
options.put('remote',robot+'/leftArm')  # we add info on to whom we will connect
options.put('local','/demo'+robot+'/leftArm')  # we add info on how we will call ourselves on the YARP network
dd = yarp.PolyDriver(options)  # create a YARP multi-use driver with the given options

pos = dd.viewIPositionControl()  # make a position controller object we call 'pos'
vel = dd.viewIVelocityControl()  # make a velocity controller object we call 'vel'
enc = dd.viewIEncoders()  # make an encoder controller object we call 'enc'
mode = dd.viewIControlMode2()  # make a operation mode controller object we call 'mode'
ll = dd.viewIControlLimits()  # make a limits controller object we call 'll'

axes = enc.getAxes()  # retrieve number of joints

# use the object to set the device to position mode (as opposed to velocity mode)(note: stops the robot)
mode.setControlModes(yarp.IVector(axes, yarp.encode('pos')))

print 'positionMove(1,-35) -> moves motor 1 (start count at motor 0) to -35 degrees'
pos.positionMove(0,-35)

print 'sleep(5)'
sleep(5)

#min = yarp.DVector(1)

