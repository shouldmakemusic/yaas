"""
# Copyright (C) 2007 Rob King (rob@re-mu.org)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Rob King <rob@e-mu.org> or visit http://www.e-mu.org

This file contains all the current Live OSC callbacks. 

"""
import Live

# OSC
from LiveOSC.OSCMessage import OSCMessage
from LiveOSC.CallbackManager import CallbackManager
from LiveOSC.OSCUtils import *

# RemixNet
import LiveOSC.OSCClient
import LiveOSC.OSCServer
import LiveOSC.UDPClient
import LiveOSC.UDPServer


class OSCCallbacks:
    def __init__(self, oscServer):
        
        print('(OSCCallbacks) init')
        if oscServer:
            self.oscServer = oscServer
            self.callbackManager = oscServer.callbackManager
            self.oscClient = oscServer.oscClient
        else:
            return

        self.callbackManager.add(self.sensorX, "/yaas/sensor")


    def sensorX(self, msg):
        """Called when a /yaas/sensor measurement is received.

        Messages:
        /yaas/sensor (float tempo)   Set the tempo, replies with /live/tempo (float tempo)
        """
        if len(msg) == 5:
            x = msg[2]
            y = msg[3]
            z = msg[4]
            print('Received values: ' + str(x) + ", " + str(y) + ", " + str(z))
            #LiveUtils.setTempo(tempo)
        

