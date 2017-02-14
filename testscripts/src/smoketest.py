
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
import unittest
from unittest import TestCase


class smoketest():

        def __init__(self,system_ip,username,password,debug_enabled,thread_lock):
            self.system_ip=system_ip
            self.username=username
            self.pwd=password
            self.debug_enabled=debug_enabled
            self.thread_lock=thread_lock

        def test_move_files(self):
            #logger(debug_enabled)
            logfile=logging.getLogger('logmain')
            logfile.info("*****************START SMOKETEST LOG***************************")
            logfile.info("PID %s" % os.getpid())

            #create device object
            self.dut=sshdevice(self.system_ip,self.username,self.pwd)
            if self.dut.connect() == False:
                return False

            self.out=self.dut.send_cmd("ls -la")
            if self.out == False:
                return False
            self.data=out.readlines()
            for self.line in self.data:
                print self.line.strip()
                #sys.stdout.write(line)

            self.out=self.dut.send_cmd('cd hello_project;ls -la')
            if self.out == False:
                return False
            self.data=self.out.readlines()
            for self.line in self.data:
                print self.line.strip()
                #sys.stdout.write(line)

            #files=os.listdir(os.curdir)
            #logfile.info(files)

            self.threadlock.acquire()
            self.logfile.info("Acquired lock")
            if self.dut.put_files("test.cpp", "/root/hello_project/test.cpp") == False:
                return False

            time.sleep(2)

            if self.dut.get_files("/root/hello_project/test.spec", "newspec.file") == False:
                return False
            self.threadlock.release()
            self.logfile.info("Released lock")

            self.threadlock.acquire()
            self.logfile.info('Acquired lock for rpm installation')
            #delete previous rpm
            self.logfile.info("Deleting previous rpm")
            if self.dut.send_cmd('rm -rf hello_project/rpmbuild/RPMS/i686/*') == False:
                return False

            #delete previous binary
            self.logfile.info("Deleting previos binary")
            if self.dut.send_cmd('rm -rf /usr/bin/helloworld') == False:
                return False

            #create new rpm
            self.logfile.info("Building new rpm")
            if self.dut.send_cmd('rpmbuild -ba hello_project/rpmbuild/SPECS/test.spec') == False:
                return False

            #verify rpm exist and is at the correct location
            self.out=self.dut.send_cmd("ls hello_project/rpmbuild/RPMS/i686/")
            if self.out == False:
                return False
            self.dline=self.out.readline()
            self.rpm_match=re.match('helloworld.*i686\.rpm',self.dline)
            if self.rpm_match == None:
                self.logfile.info("No rpm match found")
                return False
            else:
                self.rpm_name=rpm_match.group()
                self.logfile.info("Match, found rpm %s " % self.rpm_name)

            #install rpm
            self.logfile.info("Installing newly built rpm")
            if vdut.send_cmd('rpm -Uvh --force hello_project/rpmbuild/RPMS/i686/' + self.rpm_name) == False:
                return False

            #run binary installed by rpm
            self.logfile.info("Executing binary installed by rpm")
            self.out=self.dut.send_cmd('/usr/bin/helloworld')
            if out == False:
                return False
            else:
                self.logfile.info('Output of binary installed from rpm \"%s\" ' % out.readline().strip())

            self.threadlock.release()
            self.logfile.info('Released lock from rpm installation')

            self.dut.done()
            return True

            def tearDown(self):
                self.browser.close()


