import os
import ConfigParser

from ..consts import DEFAULT_PORT_LIGHTHOUSE
from ..consts import DEFAULT_OSC_RECEIVE

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
        port = self.get_lighthouse_config('port')
        if isinstance(port, ( int, long ) ):
            return int(port)
        return DEFAULT_PORT_LIGHTHOUSE
    
    def get_osc_receive(self):
        osc_receive = self.get_yaas_config('osc_receive')
        if osc_receive == 'True' or osc_receive == 'true' or osc_receive == True:
            return True
        return DEFAULT_OSC_RECEIVE
    
    def get_yaas_port(self):
        osc_port = self.get_yaas_config('osc_port')
        if osc_port.isdigit():
            return int(osc_port)
        return None
        