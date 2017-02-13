#!/usr/bin/env python

#import paramiko
import sys
import os
from logger import logger
import logging
from sshdevice import sshdevice
import ConfigParser
import multiprocessing
import time
import re

def main(params):
        (system_ip,username,pwd,debug_to_file,threadlock)=params
        logger(debug_to_file)
        logfile=logging.getLogger('logmain')
        logfile.info("*****************START LOG***************************")
        logfile.info("PID %s" % os.getpid())

        #create device object
        dut=sshdevice(system_ip,username,pwd)
        if dut.connect() == False:
            return False

        out=dut.send_cmd("ls -la")
        if out == False:
            return False
        data=out.readlines()
        for line in data:
            print line.strip()
            #sys.stdout.write(line)

        out=dut.send_cmd('cd hello_project;ls -la')
        if out == False:
            return False
        data=out.readlines()
        for line in data:
            print line.strip()
            #sys.stdout.write(line)

        #files=os.listdir(os.curdir)
        #logfile.info(files)

        threadlock.acquire()
        logfile.info("Acquired lock")
        if dut.put_files("test.cpp", "/root/hello_project/test.cpp") == False:
            return False

        time.sleep(2)

        if dut.get_files("/root/hello_project/test.spec", "newspec.file") == False:
            return False
        threadlock.release()
        logfile.info("Released lock")

        threadlock.acquire()
        logfile.info('Acquired lock for rpm installation')
        #delete previous rpm
        logfile.info("Deleting previous rpm")
        if dut.send_cmd('rm -rf hello_project/rpmbuild/RPMS/i686/*') == False:
            return False

        #delete previous binary
        logfile.info("Deleting previos binary")
        if dut.send_cmd('rm -rf /usr/bin/helloworld') == False:
            return False

        #create new rpm
        logfile.info("Building new rpm")
        if dut.send_cmd('rpmbuild -ba hello_project/rpmbuild/SPECS/test.spec') == False:
            return False

        #verify rpm exist and is at the correct location
        out=dut.send_cmd("ls hello_project/rpmbuild/RPMS/i686/")
        if out == False:
            return False
        dline=out.readline()
        rpm_match=re.match('helloworld.*i686\.rpm',dline)
        if rpm_match == None:
            logfile.info("No rpm match found")
            return False
        else:
            rpm_name=rpm_match.group()
            logfile.info("Match, found rpm %s " % rpm_name)

        #install rpm
        logfile.info("Installing newly built rpm")
        if dut.send_cmd('rpm -Uvh --force hello_project/rpmbuild/RPMS/i686/' + rpm_name) == False:
            return False

        #run binary installed by rpm
        logfile.info("Executing binary installed by rpm")
        out=dut.send_cmd('/usr/bin/helloworld')
        if out == False:
            return False
        else:
            logfile.info('Output of binary installed from rpm \"%s\" ' % out.readline().strip())

        threadlock.release()
        logfile.info('Released lock from rpm installation')

        dut.done()
        return True


if __name__ == '__main__':

    #init config parser to read all the systems to be tested
    iniparser=ConfigParser.ConfigParser()
    iniparser.read('systems.ini')
    number_of_systems=iniparser.getint('config','count')
    bool_log_to_file=iniparser.getboolean('config','debug')

    #create logging object first time
    logger(bool_log_to_file)
    logfile=logging.getLogger('logmain')
    systems_list=[]
    failures=0

    threadpool=multiprocessing.Pool()
    threadlock=multiprocessing.Manager().Lock()

    #loop thru the systems in the ini file
    for i in range(1,number_of_systems+1):
        systems_list+=[(iniparser.get('s'+str(i),'ip'),iniparser.get('s'+str(i),'username'),iniparser.get('s'+str(i),'pwd'),bool_log_to_file,threadlock)]

    results=threadpool.map(main, systems_list)
    logfile.info("Done running all threads")
    threadpool.close()
    threadpool.join()

    logfile.info("Getting exit code for threads")
    for (ip,user,pwd,debug_value,tlock),retcode in zip(systems_list,results):
        logfile.info('%s %s %s %s' % (retcode,ip,user,pwd))
        if retcode == False:
            failures+=1

    if failures != 0:
        logfile.error("There were %s failures in a thread(s), please check log" % failures)
        sys.exit(False)
    else:
        logfile.info("Done running smoke test, found no failures")
        sys.exit(True)



