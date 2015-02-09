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
from OSCMessage import OSCMessage
from CallbackManager import CallbackManager
from OSCUtils import *



if __name__ == "__main__":
    hexDump("Welcome to the OSC testing program.")
    print
    message = OSCMessage()
    message.setAddress("/foo/play")
    message.append(44)
    message.append(11)
    message.append(4.5)
    message.append("the white cliffs of dover")
    hexDump(message.getBinary())

    print "Making and unmaking a message.."

    strings = OSCMessage()
    strings.append("Mary had a little lamb")
    strings.append("its fleece was white as snow")
    strings.append("and everywhere that Mary went,")
    strings.append("the lamb was sure to go.")
    strings.append(14.5)
    strings.append(14.5)
    strings.append(-400)

    raw  = strings.getBinary()

    hexDump(raw)
    
    print "Retrieving arguments..."
    data = raw
    for i in range(6):
        text, data = readString(data)
        print text

    number, data = readFloat(data)
    print number

    number, data = readFloat(data)
    print number

    number, data = readInt(data)
    print number

    hexDump(raw)
    print decodeOSC(raw)
    print decodeOSC(message.getBinary())

    print "Testing Blob types."
   
    blob = OSCMessage() 
    blob.append("","b")
    blob.append("b","b")
    blob.append("bl","b")
    blob.append("blo","b")
    blob.append("blob","b")
    blob.append("blobs","b")
    blob.append(42)

    hexDump(blob.getBinary())

    print decodeOSC(blob.getBinary())

    def printingCallback(stuff):
        sys.stdout.write("Got: ")
        for i in stuff:
            sys.stdout.write(str(i) + " ")
        sys.stdout.write("\n")

    print "Testing the callback manager."
    
    c = CallbackManager()
    c.add(printingCallback, "/print")
    
    c.handle(message.getBinary())
    message.setAddress("/print")
    c.handle(message.getBinary())
    
    print1 = OSCMessage()
    print1.setAddress("/print")
    print1.append("Hey man, that's cool.")
    print1.append(42)
    print1.append(3.1415926)

    c.handle(print1.getBinary())

    bundle = OSCMessage()
    bundle.setAddress("")
    bundle.append("#bundle")
    bundle.append(0)
    bundle.append(0)
    bundle.append(print1.getBinary(), 'b')
    bundle.append(print1.getBinary(), 'b')

    bundlebinary = bundle.message

    print "sending a bundle to the callback manager"
    c.handle(bundlebinary)
