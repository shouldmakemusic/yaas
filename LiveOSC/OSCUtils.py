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

def hexDump(bytes):
    """Useful utility; prints the string in hexadecimal"""
    for i in range(len(bytes)):
        sys.stdout.write("%2x " % (ord(bytes[i])))
        if (i+1) % 8 == 0:
            print repr(bytes[i-7:i+1])

    if(len(bytes) % 8 != 0):
        print string.rjust("", 11), repr(bytes[i-7:i+1])

def readString(data):
    length   = string.find(data,"\0")
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    return (data[0:length], data[nextData:])


def readBlob(data):
    length   = struct.unpack(">i", data[0:4])[0]    
    nextData = int(math.ceil((length) / 4.0) * 4) + 4   
    return (data[4:length+4], data[nextData:])


def readInt(data):
    if(len(data)<4):
        print "Error: too few bytes for int", data, len(data)
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest    = data[4:]
        
    return (integer, rest)



def readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer."""
    high, low = struct.unpack(">ll", data[0:8])
    big = (long(high) << 32) + low
    rest = data[8:]
    return (big, rest)



def readFloat(data):
    if(len(data)<4):
        print "Error: too few bytes for float", data, len(data)
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest  = data[4:]

    return (float, rest)


def OSCBlob(next):
    """Convert a string into an OSC Blob,
    returning a (typetag, data) tuple."""

    if type(next) == type(""):
        length = len(next)
        padded = math.ceil((len(next)) / 4.0) * 4
        binary = struct.pack(">i%ds" % (padded), length, next)
        tag    = 'b'
    else:
        tag    = ''
        binary = ''
    
    return (tag, binary)


def OSCArgument(next):
    """Convert some Python types to their
    OSC binary representations, returning a
    (typetag, data) tuple."""
    
    if type(next) == type(""):        
        OSCstringLength = math.ceil((len(next)+1) / 4.0) * 4
        binary  = struct.pack(">%ds" % (OSCstringLength), next)
        tag = "s"
    elif type(next) == type(42.5):
        binary  = struct.pack(">f", next)
        tag = "f"
    elif type(next) == type(13):
        binary  = struct.pack(">i", next)
        tag = "i"
    else:
        binary  = ""
        tag = ""

    return (tag, binary)


def parseArgs(args):
    """Given a list of strings, produces a list
    where those strings have been parsed (where
    possible) as floats or integers."""
    parsed = []
    for arg in args:
        print arg
        arg = arg.strip()
        interpretation = None
        try:
            interpretation = float(arg)
            if string.find(arg, ".") == -1:
                interpretation = int(interpretation)
        except:
            # Oh - it was a string.
            interpretation = arg
            pass
        parsed.append(interpretation)
    return parsed



def decodeOSC(data):
    """Converts a typetagged OSC message to a Python list."""
    table = {"i":readInt, "f":readFloat, "s":readString, "b":readBlob}
    decoded = []
    address,  rest = readString(data)
    typetags = ""

    if address == "#bundle":
        time, rest = readLong(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest)>0:
            length, rest = readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest)>0:
        typetags, rest = readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if(typetags[0] == ","):
            for tag in typetags[1:]:
                value, rest = table[tag](rest)                
                decoded.append(value)
        else:
            print "Oops, typetag lacks the magic ,"

    # return only the data
    return decoded

