#!/usr/bin/env python

import yarp

class ButtonResponder(yarp.PortReader):
    def __init__(self, ipwm):
        yarp.PortReader.__init__(self)
        self.ipwm = ipwm

    def read(self, connection):
        b = yarp.Bottle()

        if not connection.isValid() or not b.read(connection) or b.size() != 2:
            return False

        if b.get(0).asBool():
            ipwm.setRefDutyCycle(0, 100.0)
        elif b.get(1).asBool():
            ipwm.setRefDutyCycle(0, -100.0)

        return True

yarp.Network.init()

if not yarp.Network.exists('/spacenavigator/buttons'):
    print('Remote port /spacenavigator/buttons does not exist.')
    quit()

lacquey = yarp.PolyDriver()
buttonPort = yarp.Port()

try:
    options = yarp.Property()
    options.put('device', 'remote_controlboard')
    options.put('remote', '/teo/rightHand')
    options.put('local', '/lacqueyGrip')

    if not lacquey.open(options): quit()

    buttonResponder = ButtonResponder(lacquey.viewIPWMControl())
    buttonPort.setReader(buttonResponder)

    if not buttonPort.open('/lacqueyGrip/buttons'): quit()
    if not yarp.Network.connect('/spacenavigator/buttons', buttonPort.getName()): quit()

    while True: pass

finally:
    buttonPort.close()
    lacquey.close()
    yarp.Network.fini()
