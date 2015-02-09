"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
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
# Nathan Ramella <nar@remix.net> or visit http://www.liveapi.org

RemixNet Module

This module contains four classes that have been assembled to facilitate
remote control of Ableton Live. It's been an interesting experience learning
Python and has given me a lot of time to think about music and networking
protocols. I used OSC as it's somewhat of an accepted protocol and at least
more flexible than MIDI. It's not the quickest protocol in terms of
pure ops, but it gets the job done. 

For most uses all you'll need to do is create an OSCServer object, it
in turn creates an OSCClient and registers a couple default callbacks
for you to test with. Both OSCClient and OSCServer create their own UDP
sockets this is settable on initialization and during runtime if you wish
to change them.

Any input or feedback on this code will always be appreciated and I look 
forward to seeing what will come next.

-Nathan Ramella (nar@remix.net)

-Updated 29/04/09 by ST8 (st8@q3f.org)
    Works on Mac OSX with Live7/8
    
    The socket module is missing on osx and including it from the default python install doesnt work.
    Turns out its the os module that causes all the problems, removing dependance on this module and 
    packaging the script with a modified version of the socket module allows it to run on osx.
    
"""

import inspect
import os
import sys
import Live

# Import correct paths for os / version
version = Live.Application.get_application().get_major_version()
if sys.platform == "win32":
    import socket   

else:
    if version > 7:
       # 10.5
        try:
            file = open("/usr/lib/python2.5/string.pyc")
        except IOError:
            sys.path.append("/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5")
            import socket_live8 as socket  
        else:
            sys.path.append("/usr/lib/python2.5")
            import socket

# OSC
from OSCMessage import OSCMessage
from CallbackManager import CallbackManager
from OSCUtils import *
    
class UDPServer:

    """
    RemixNet.UDPServer
       
    This class is a barebones UDP server setup with the ability to
    assign callbacks for incoming data. In the design as is, we use
    an OSC.CallbackManager when we recieve any data.
      
    This class is designed to be used by RemixNet.OSCServer, as it
    will do all the setup for you and register a few default OSCManager
    callbacks.
    """
       
    def __init__(self, src, srcPort):
        """
        Sets up the UDPServer component of this package. By default 
        we listen to all interfaces on port 9000 for incoming requests 
        with a 4096 byte buffer.
        
        You can modify these settings by using the methods setport() and setHost()
        """
        
        if srcPort:
            self.srcPort = srcPort
        else:
            self.srcPort = 9000 
        
        if src:
            self.src = src
        else:
            self.src = ''
        
        self.buf = 4096

    def processIncomingUDP(self):
        """
        Attempt to process incoming packets in the network buffer. If none are
        available it will return. If there is data, and a callback manager has been
        defined we'll send the data to the callback manager. 
        
        You can specify a callback manager using the UDPServer.setCallbackManager() 
        function and passing it a populated OSC.Manager object.
        """
        
        try:
            # You'd think this while 1 loop would get stuck and block the
            # program. But. As it turns out. It doesn't. 
            
            while 1:
                self.data,self.addr = self.UDPSock.recvfrom(self.buf)
                if not self.data:
                # No data buffered this round!
                    return
                else:
                    if self.data != '\n':
                        # Oh snap, we have data!
                        # If you want to write your own special handlers for dealing
                        # with incoming data, this is the place. self.data contains
                        # the raw data sent to our UDP socket.
                        
                        print('UDP raw: ' + self.data)
                
                        if self.callbackManager:
                            self.callbackManager.handle(self.data)
                        
        except Exception, e:
            pass

    def setCallbackManager(self, callbackManager):
        """
        You can specify a callbackManager here as derived from OSC.py. 
        We use this function in OSCServer to register the default /remix/
        namespace addresses as utility callbacks.
        """
        
        self.callbackManager = callbackManager

    def bind(self):
        """
        After initializing you must UDPServer.listen() to bind to the socket
        and accept whatever packets are in the buffer. Since we're binding a 
        non-blocking socket, your program (and Ableton Live) will still be 
        able to run.
        """
        
        self.addr = (self.src,self.srcPort)
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDPSock.bind(self.addr)
        self.UDPSock.setblocking(0)

    def close(self):
        """ 
        Close our UDPSock
        """
        # Closing time!
        self.UDPSock.close()
