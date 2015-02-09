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
      
class OSCClient:
    """
    This is a helperclass for the OSCServer that will setup
    a simple method for sending OSC messages
    """
    
    def __init__(self, udpClient=None, address=None, msg=None):
        """
        Initializes a RemixNet.OSCClient object. You can pass
        in a default address or default msg here. This is useful
        for making 'beacon' clients that you can attach as
        listeners on Live object attributes.
        """
    
        if address is not None:
            self.address = address
            
        if msg:
            self.msg = msg
	else:
	    self.msg = None
            
        if udpClient is not None:
            self.udpClient = udpClient
            
    def setUDPClient(self, udpClient):
        """
        If we create our OSCClient object without defining a udpClient
        we can set one after the fact here. If you don't and you try to
        send, you'll raise an exception.
        """
        
        if udpClient:
            self.udpClient = udpClient
        
    def send(self, address=None, msg=None):
       
        """
        Given an OSC address and OSC msg payload we construct our
        OSC packet and send it to its destination. You can pass in lists
        or tuples in msg and we will iterate over them and append each 
        to the end of a single OSC packet.
        
        This can be useful for transparently dealing with methods that
        yield a variety of values in a list/tuple without the necessity of
        combing through it yourself.
        """
        
        if self.udpClient is None:
            # SHOULD RAISE EXCEPTION
            return
        
        
        # If neither address or msg, we have nothing to do.
        
        if not address and not self.address:
            # SHOULD RAISE EXCEPTION
            return
        
        # I feel a little weird doing this, but I want to keep
        # the 'default' self.msg that the object was initialized
        # with, without playing Towers of Hanoi with another variable.
        
        if self.msg and self.msg is not None:
            msg = self.msg
        
        # I don't like doing it here any more than I did up there.
           
        if not address:
            if not self.address:
                # SHOULD RAISE EXCEPTION
                return
            address = self.address

        oscMessage = OSCMessage()
        oscMessage.setAddress(address)

        # We need to check for msgs that are actually
        # instance methods here and do something with
        # them...
        # if type(msg) == instance method:
        # blahblah
        
        # By default OSC.py doesn't look like it'll process tuples
        # and pack them. So, we help it along by breaking them up
        # and appending each entity.
       
        if type(msg) in (str,int,float):
           oscMessage.append(msg)
        elif type(msg) in (list,tuple):
             for m in msg:
                if type(m) not in (str,int,float):
                    # SHOULD RAISE EXCEPTION
                    return
                oscMessage.append(m)      
        elif msg == None:
        	self.udpClient.send(oscMessage.getBinary())
		return
        else:
            # SHOULD RAISE EXCEPTION
            # Likely, method or instancemethod object. We should
            # actually execute the code here and send the result,
            # but for now we'll just return.
            return
        # Done processing, send it off to its destination            
       	self.udpClient.send(oscMessage.getBinary())
        