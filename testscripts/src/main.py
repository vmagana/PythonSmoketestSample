#!/usr/bin/env python

#import paramiko
import sys
import os
from logger import logger
import logging
#from sshdevice import sshdevice
import ConfigParser
import multiprocessing
import time
import re
import unittest
from smoketest import smoketest

def main(params):
        (system_ip,username,pwd,debug_enabled,thread_lock)=params
        logger(debug_enabled)
        logfile=logging.getLogger("logmain")
        logfile.info("*****************START LOG***************************")

        run_test=smoketest(system_ip,username,pwd,debug_enabled,thread_lock)
        if run_test.test_move_files() == False:
            return False
        else:
            return True



if __name__ == '__main__':

    #init config parser to read all the systems to be tested
    iniparser=ConfigParser.ConfigParser()
    iniparser.read("systems.ini")
    number_of_systems=iniparser.getint("config","count")
    debug_enabled=iniparser.getboolean("config","debug")

    #create logging object first time
    logger(debug_enabled)
    logfile=logging.getLogger("logmain")
    systems_list=[]
    failures=0

    threadpool=multiprocessing.Pool()
    thread_lock=multiprocessing.Manager().Lock()

    #loop thru the systems in the ini file
    for i in range(1,number_of_systems+1):
        systems_list+=[(iniparser.get("s"+str(i),"ip"),iniparser.get("s"+str(i),"username"),iniparser.get("s"+str(i),"pwd"),debug_enabled,thread_lock)]

    results=threadpool.map(main, systems_list)
    logfile.info("Done running all threads")
    threadpool.close()
    threadpool.join()

    logfile.info("Getting exit code for threads")
    for (ip,user,pwd,debug_value,tlock),retcode in zip(systems_list,results):
        logfile.info("%s %s %s %s" % (retcode,ip,user,pwd))
        if retcode == False:
            failures+=1

    if failures != 0:
        logfile.error("There were %s failures in a thread(s), please check log" % failures)
        sys.exit(False)
    else:
        logfile.info("Done running smoke test, found no failures")
        sys.exit(True)



