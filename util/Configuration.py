import os
import ConfigParser

# https://wiki.python.org/moin/ConfigParserExamples
class Configuration:
    """
        Loads configurations and makes it available
    """
    __module__ = __name__
    __doc__ = "Loads configurations and makes it available"
    
    def __init__(self, yaas):
        self.yaas = yaas
        self.log = yaas.log
        self.log.debug('(Configuration) init')
        
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(os.path.join(os.path.dirname(__file__), '..', 'default.cfg')))
        self.log.verbose('(Configuration) sections: ' + str(self.config.sections()))
        others = self.map('Others')
        self.log.info('Configuration others ' + str(others))
        self.log.info('(Configuration) test ' + others['route'])
        self.log.info('(Configuration) test ' + others['midi_note_definitions'])
        midi_note_definitions = eval(others['midi_note_definitions'])
        self.log.info('Configuration test ' + str(midi_note_definitions[6][0]))
        
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
