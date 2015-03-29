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
"""
    Loads configurations and makes it available
"""
import os
import ConfigParser

from ..consts import DEFAULT_PORT_LIGHTHOUSE
from ..consts import DEFAULT_OSC_RECEIVE
from ..consts import DEFAULT_SHOW_RED_FRAME
from ..consts import PREV
from ..consts import NEXT
from ..consts import CURRENT

# https://wiki.python.org/moin/ConfigParserExamples
class Configuration:
    """
        Loads configurations and makes it available
    """
    __module__ = __name__
    __doc__ = "Loads configurations and makes it available"
    
    def __init__(self, yaas):
        
        if yaas is not None:
            self.log = yaas.log
            self.log.debug('(Configuration) init')
        else:
            self.log = None
        
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(os.path.join(os.path.dirname(__file__), 'default.cfg')))
        self.config_lighthouse = self.map('LightHouse')
        self.config_yaas = self.map('YAAS')
        
        if self.log is not None:
            self.log.debug('(Configuration) lh port: ' + str(self.get_lighthouse_port()))
            self.log.verbose('(Configuration) sections: ' + str(self.config.sections()))
        #midi_note_definitions = eval(others['midi_note_definitions'])
        
    def map(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    self.log.verbose("skip: %s" % option)
            except:
                self.log.error("exception on %s!" % option)
                dict1[option] = None
        return dict1
    
    def get(self, section, option):
        return self.config.get(section, option)
        
    def get_lighthouse_config(self, option):
        return self.config_lighthouse[option]
    
    def get_yaas_config(self, option):
        return self.config_yaas[option]
        
    def get_lighthouse_port(self):
        """
            Returns the port for outgoing messages (default 9050)
        """
        port = self.get_lighthouse_config('port')
        if isinstance(port, ( int, long ) ):
            return int(port)
        return DEFAULT_PORT_LIGHTHOUSE
    
    def get_osc_receive(self):
        """
            Returns if YAAS should also receive osc (default None)
        """
        osc_receive = self.get_yaas_config('osc_receive')
        if osc_receive == 'True' or osc_receive == 'true' or osc_receive == True:
            return True
        return DEFAULT_OSC_RECEIVE
    
    def get_yaas_port(self):
        """
            Returns the port for incoming messages (default None)
        """
        osc_port = self.get_yaas_config('osc_port')
        if osc_port.isdigit():
            return int(osc_port)
        return None
    
    def get_midi_note_definitions_lighthouse(self):
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.join(os.path.dirname(__file__), 'midi_from_lighthouse.cfg')))
            definitions = eval(config.get('Definitions', 'midi_note_definitions_lighthouse'))
            definitions = self.replace_constants(definitions)
            return definitions
        except Exception, err:
            self.log.error("Could not read from midi_from_lighthouse.cfg: " + str(err))

    def get_midi_note_definitions(self):
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.join(os.path.dirname(__file__), 'midi_mapping.cfg')))
            definitions = eval(config.get('MidiIn', 'midi_note_definitions'))
            definitions = self.replace_constants(definitions)
            return definitions
        except Exception, err:
            self.log.error("Could not read from midi_mapping.cfg: " + str(err))

    def get_midi_note_off_definitions(self):
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.join(os.path.dirname(__file__), 'midi_mapping.cfg')))
            definitions = eval(config.get('MidiIn', 'midi_note_off_definitions'))
            definitions = self.replace_constants(definitions)
            return definitions
        except Exception, err:
            self.log.error("Could not read from midi_mapping.cfg: " + str(err))

    def get_midi_cc_definitions(self):
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.join(os.path.dirname(__file__), 'midi_mapping.cfg')))
            definitions = eval(config.get('CC', 'midi_cc_definitions'))
            definitions = self.replace_constants(definitions)
            return definitions
        except Exception, err:
            self.log.error("Could not read from midi_mapping.cfg (cc): " + str(err))

    def red_frame_visible(self):
        """
            Returns if yaas should show a red frame for selecting clips
        """        
        self.log.verbose("(Configuration) red_frame_visible")
        show_red_frame = self.get_yaas_config('red_frame_visible')
        if eval(show_red_frame) == True:
            self.log.verbose("(Configuration) = True")
            return True
        if eval(show_red_frame) == False:
            self.log.verbose("(Configuration) = False")
            return False
        self.log.verbose("(Configuration) = " + str(DEFAULT_SHOW_RED_FRAME))
        return DEFAULT_SHOW_RED_FRAME
        
    def red_frame_fixed_on_top(self):
        """
            Returns if the red frame should always stay on top (first scene)
        """        
        self.log.verbose("(Configuration) red_frame_fixed_on_top")
        red_frame_fixed_on_top = self.get_yaas_config('red_frame_fixed_on_top')
        if eval(red_frame_fixed_on_top) == True:
            self.log.verbose("(Configuration) = True")
            return True
        if eval(red_frame_fixed_on_top) == False:
            self.log.verbose("(Configuration) = False")
            return False
        return True
        
    def red_frame_width(self):
        """
            Returns the width of the red frame
        """        
        self.log.verbose("(Configuration) red_frame_width")
        red_frame_width = self.get_yaas_config('red_frame_width')
        return int(red_frame_width)
        
    def red_frame_height(self):
        """
            Returns the height of the red frame
        """        
        self.log.verbose("(Configuration) red_frame_height")
        red_frame_height = self.get_yaas_config('red_frame_height')
        return int(red_frame_height)
        
    def replace_constants(self, definitions):
        
        for k, v in definitions.iteritems():
            params = definitions[k][2]
            #self.log.verbose('(Configuration) ' + str(params))
            for i in range(len(params)):
                if params[i] == 'CURRENT':
                    params[i] = CURRENT
                elif params[i] == 'PREV':
                    params[i] = PREV
                elif params[i] == 'NEXT':
                    params[i] = NEXT
                elif params[i] == 'True' or params[i] == 'true':
                    params[i] = True
                elif params[i] == 'False' or params[i] == 'false':
                    params[i] = False
                elif isinstance(params[i], ( int, long ) ):
                    params[i] = int(params[i])
        return definitions
        