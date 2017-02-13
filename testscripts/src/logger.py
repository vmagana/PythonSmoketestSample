import logging
import os
import sys
import re

class logger(object):

    def __init__(self,log_to_file=False):
        self.log_to_file=log_to_file

        if self.log_to_file == True:
            logging.basicConfig(filename=re.sub('\.\w+', '.log', __file__), \
            format='%(levelname)s %(asctime)s %(threadName)s %(message)s', \
            datefmt='%m/%d/%Y %I:%M:%S %p', \
            level=logging.DEBUG, \
            filemode='w')
            logfile=logging.getLogger('logmain')
            logfile.setLevel(logging.DEBUG)
            textformat=logging.Formatter('%(levelname)s %(asctime)s %(threadName)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
            console=logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            console.setFormatter(textformat)
            logfile.addHandler(console)
        else:
            logfile=logging.getLogger('logmain')
            textformat=logging.Formatter('%(levelname)s %(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
            console=logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            console.setFormatter(textformat)
            logfile.addHandler(console)
            logfile.setLevel(logging.INFO)


