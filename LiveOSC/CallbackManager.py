#!/usr/bin/python
#
# Open SoundControl for Python
# Copyright (C) 2002 Daniel Holth, Clinton McChesney
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
# Daniel Holth <dholth@stetson.edu> or visit
# http://www.stetson.edu/~ProctoLogic/
#
# Changelog:
# 15 Nov. 2001:
#   Removed dependency on Python 2.0 features.
#   - dwh
# 13 Feb. 2002:
#   Added a generic callback handler.
#   - dwh

import sys
import struct
import math
import string
import OSCMessage
from OSCUtils import *

class CallbackManager:
    """This utility class maps OSC addresses to callables.

    The CallbackManager calls its callbacks with a list
    of decoded OSC arguments, including the address and
    the typetags as the first two arguments."""

    def __init__(self):
        self.callbacks = {}
        self.add(self.unbundler, "#bundle")

    def handle(self, data, source = None):
        """Given OSC data, tries to call the callback with the
        right address."""
        decoded = decodeOSC(data)
        self.dispatch(decoded)

    def dispatch(self, message):
        """Sends decoded OSC data to an appropriate calback"""
        try:
            address = message[0]
            self.callbacks[address](message)
        except KeyError, e:
	    print "key not found"
            # address not found
            pass
        except None, e:
            print "Exception in", address, "callback :", e
        
        return

    def add(self, callback, name):
        """Adds a callback to our set of callbacks,
        or removes the callback with name if callback
        is None."""
        if callback == None:
            del self.callbacks[name]
        else:
            self.callbacks[name] = callback
            print 'added callback ' + name

    def unbundler(self, messages):
        """Dispatch the messages in a decoded bundle."""
        # first two elements are #bundle and the time tag, rest are messages.
        for message in messages[2:]:
            self.dispatch(message)
