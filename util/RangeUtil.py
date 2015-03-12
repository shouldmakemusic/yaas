"""
# Copyright (C) 2015 Manuel Hirschauer (manuel@hirschauer.net)
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
# Manuel Hirschauer <manuel@hirschauer.net> 

This file contains the RangeUtil that converts numbers in ranges to the target ableton range

"""

class RangeUtil:
    
    def __init__(self, source_min_value, source_max_value):
        
        self.source_min_value = source_min_value
        self.source_max_value = source_max_value
    
    def set_target_min_max(self, target_min_value, target_max_value):
        
        self.target_min_value = target_min_value
        self.target_max_value = target_max_value
        
    def get_factor(self):
        
        range1 = self.target_max_value - self.target_min_value
        #print "range1=" + str(range1)
        range2 = self.source_max_value - self.source_min_value
        #print "range2=" + str(range2)
        factor = 1.0 * range1/range2
        #print factor
        return factor
        
    def get_target_value(self, source_value):
        
        factor = self.get_factor()
        return (source_value * factor) + abs(factor * self.source_min_value) - abs(self.target_min_value)
    
    def get_value(self, device_parameter, source_value):
        #print('Setting min: ' + str(device_parameter.min)) 
        self.target_min_value = device_parameter.min
        #print('Setting max: ' + str(device_parameter.max)) 
        self.target_max_value = device_parameter.max
        return self.get_target_value(source_value)
    
if __name__ == "__main__":
    print("Welcome to the Range Util testing program.")
    print
    range_util = RangeUtil(0, 10)
    range_util.set_target_min_max(0, 5)
    print("Setup source range from 0 to 10")
    print("target range is from 0 to 5")
    
    target_value = range_util.get_target_value(5)
    print("val: 5, exp: 2.5, is " + str(target_value))
     
    target_value = range_util.get_target_value(10)
    print("val: 10, exp: 5, is " + str(target_value))
     
    target_value = range_util.get_target_value(0)
    print("val: 0, exp: 2.5, is " + str(target_value))
     
    range_util = RangeUtil(-10, 10)
    range_util.set_target_min_max(0, 5)
    print("Setup source range from -10 to 10")
    print("target range is from 0 to 5")
    
    target_value = range_util.get_target_value(0)
    print("val: 0, exp: 2.5, is " + str(target_value))

    target_value = range_util.get_target_value(10)
    print("val: 10, exp: 5, is " + str(target_value))

    target_value = range_util.get_target_value(-10)
    print("val: -10, exp: 0, is " + str(target_value))

    range_util = RangeUtil(-10, 10)
    range_util.set_target_min_max(-5, 5)
    print("Setup source range from -10 to 10")
    print("target range is from -5 to 5")
    
    target_value = range_util.get_target_value(0)
    print("val: 0, exp: 0, is " + str(target_value))

    target_value = range_util.get_target_value(10)
    print("val: 10, exp: 5, is " + str(target_value))

    target_value = range_util.get_target_value(-10)
    print("val: -10, exp: -5, is " + str(target_value))

    target_value = range_util.get_target_value(5)
    print("val: 5, exp: 2.5, is " + str(target_value))

    range_util = RangeUtil(-10, 10)
    range_util.set_target_min_max(0, 1)
    print("Setup source range from -10 to 10")
    print("target range is from 0 to 1")
    
    target_value = range_util.get_target_value(0)
    print("val: 0, exp: 0.5, is " + str(target_value))

    target_value = range_util.get_target_value(10)
    print("val: 10, exp: 1, is " + str(target_value))

    target_value = range_util.get_target_value(-10)
    print("val: -10, exp: 0, is " + str(target_value))

    target_value = range_util.get_target_value(5)
    print("val: 5, exp: 0.75, is " + str(target_value))

    target_value = range_util.get_target_value(-0.670376479626)
    print("val: -0.670376479626, exp: ?, is " + str(target_value))

    range_util = RangeUtil(-10, 10)
    range_util.set_target_min_max(0, 127)
    print("Setup source range from -10 to 10")
    print("target range is from 0 to 127")

    target_value = range_util.get_target_value(9.65342140198)
    print("val: 9.65342140198, exp: ?, is " + str(target_value))

