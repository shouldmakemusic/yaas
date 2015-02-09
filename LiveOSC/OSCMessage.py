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
from OSCUtils import *

class OSCMessage:
    """Builds typetagged OSC messages."""
    def __init__(self):
        self.address  = ""
        self.typetags = ","
        self.message  = ""

    def setAddress(self, address):
        self.address = address

    def setMessage(self, message):
	self.message = message

    def setTypetags(self, typetags):
	self.typetags = typetags

    def clear(self):
	self.address  = ""
	self.clearData()

    def clearData(self):
        self.typetags = ","
        self.message  = ""

    def append(self, argument, typehint = None):
        """Appends data to the message,
        updating the typetags based on
        the argument's type.
        If the argument is a blob (counted string)
        pass in 'b' as typehint."""

        if typehint == 'b':
            binary = OSCBlob(argument)
        else:
            binary = OSCArgument(argument)

        self.typetags = self.typetags + binary[0]
        self.rawAppend(binary[1])

    def rawAppend(self, data):
        """Appends raw data to the message.  Use append()."""
        self.message = self.message + data

    def getBinary(self):
        """Returns the binary message (so far) with typetags."""
        address  = OSCArgument(self.address)[1]
        typetags = OSCArgument(self.typetags)[1]
        return address + typetags + self.message

    def __repr__(self):
        return self.getBinary()
