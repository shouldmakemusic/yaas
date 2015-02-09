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
    
         
class UDPClient:
    """
    This is a fairly brain-dead UDPClient implementation that is
    used by the OSCClient to send packets out. You shouldn't need
    this unless you want to get tricky or make a linewire protocol.
    """ 
             
    def __init__(self, dst=None, dstPort=None):
        """
        When the OSCClient instantiates its UDPClient it passes along:
        - dst: The destination host. If none only send to localhost.
        - dstPort: The destination port. If none, 9001 by default.
        """
                
        if dst: 
            self.dst = dst 
        else:
            # If you'd like to try broadcast,
            # set this to <broadcast>
            # I've been unable to get it to work.
            self.dst = 'localhost' 
                                   
        if dstPort:               
            self.dstPort = dstPort
        else: 
            self.dstPort = 9001
                        
    def setDstPort(self, dstPort=None):
        """
        If the port gets reset midstream, close down our UDPSock
        and reopen to be sure. A little redundant.
        """

        # Manually set the port before init
        if not dstPort:
            return    
           
        self.DstPort = DstPort
        
        if self.UDPSock:
            self.UDPSock.close()
            self.open()
            
      
         
    def setDst(self, dst=None):
        """
        If the dst gets reset midstream, we close down our UDPSock 
        and reopen. A little redundant.
        """
        
        if not dst:
            return 
        
        self.dst = dst     
        
        if self.UDPSock:
            self.UDPSock.close()
            self.open()
            
      
                
    def open(self):
        """
        Open our UDPSock for listening, sets self.UDPSock
        """
        
        if not self.dst:
            return
        if not self.dstPort:
            return
        
        # Open up our socket, we're ready for business!
        
        self.addr = (self.dst,self.dstPort) 
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
       
        #Broadcast doesn't work for answering callbacks for some reason.
        #But, I'll leave this here if you'd like to try.
        #if self.dst == '<broadcast>':
        #    self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
        
    def send(self, data):
        """
        If we have data to send, send it, otherwise return.
        """
        # Only send if we have data.
        if not data == '':
            self.UDPSock.sendto(data,self.addr)
            data = ''
            
    def close(self):
        """ 
        Close our UDPSock
        """
        # Closing time!
        self.UDPSock.close()
       