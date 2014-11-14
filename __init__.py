#__init__.py
import sys
import os
import inspect

from YAAS import YAAS
    
log_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "/logs")
errorLog = open(log_folder + "/stderr.txt", "w", 0)
sys.stderr = errorLog
errorLog.write("Starting Error Log")

stdoutLog = open(log_folder + "/stdout.txt", "w", 0)
sys.stdout = stdoutLog
stdoutLog.write("Starting Standard Out Log")

def create_instance(c_instance):
    return YAAS(c_instance)

