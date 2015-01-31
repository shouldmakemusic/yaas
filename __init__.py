#__init__.py
import sys
import os
import inspect

from YAAS import YAAS
from util.Logger import Logger

log_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
errorLog = open(log_folder + "/stderr.txt", "w", 0)
sys.stderr = errorLog
errorLog.write("Starting Error Log")

# this does not work - ableton crashes but it would be so cool
#logger = Logger()
# sys.stderr = logger

def create_instance(c_instance):
    return YAAS(c_instance)

