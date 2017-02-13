import paramiko
import sys
import os
import logging

class sshdevice(object):

    def __init__(self,ip,user,pwd):
        self.ip=ip
        self.user=user
        self.pwd=pwd

        self.logfile=logging.getLogger('logmain')

    def connect(self):
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            #ssh.connect(ip, username=user, key_filename=key_file)
            self.ssh.connect(self.ip,username=self.user,password=self.pwd,timeout=5)
            self.logfile.info("Succesfully Connected to device: %s " % self.ip)
            return True
        except Exception, e:
            self.logfile.error("Failed to connect to device: %s %s %s" % (self.ip,e.__class__,str(e)))
            return False
            #sys.exit(1)


    def send_cmd(self,cmd):
        stdin,stdout,stderr=self.ssh.exec_command(cmd)
        if stdout.channel.recv_exit_status() != 0:
            self.logfile.info("Error running command: %s, exit code: %s - %s" % \
            (cmd,stdout.channel.recv_exit_status(),os.strerror(stdout.channel.recv_exit_status())))
            return False
            #sys.exit(stdout.channel.recv_exit_status())

        return stdout

    def put_files(self,localfile,remotefile):
        try:
            self.ftp=self.ssh.open_sftp()
            self.ftp.put(localfile,remotefile)
            self.logfile.info("Successfully moved file %s to %s" % (localfile,remotefile))
            return True
        except Exception,e:
            self.logfile.error("PutFile caught exception %s - %s" % (e.__class__,e))
            return False
            #sys.exit(os.errno.ENOENT)
        finally:
            self.logfile.info("CLOSING FTP PUT")
            self.ftp.close()

    def get_files(self,remotefile,localfile):
        try:
            self.ftp=self.ssh.open_sftp()
            self.ftp.get(remotefile,localfile)
            self.logfile.info("Successfully received file from %s to %s" % (remotefile,localfile))
            return True
        except Exception,e:
            self.logfile.error("GetFile caught exception %s - %s" % (e.__class__,e))
            return False
            #sys.exit(os.errno.ENOENT)
        finally:
            self.logfile.info("CLOSING FTP GET")
            self.ftp.close()


    def done(self):
        self.ssh.close()
        self.logfile.info("Closed connection with device %s " % self.ip)



