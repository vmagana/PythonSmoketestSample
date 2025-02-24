import paramiko
import sys
import os
import logging
#from scp import SCPClient
import scp
import time

class sshdevice(object):

    def __init__(self,ip,user,pwd):
        self.ip=ip
        self.user=user
        self.pwd=pwd

        self.logfile=logging.getLogger("logmain")

    def test_rmove_files(self):
            #self.logger(self.debug_enabled)
            self.logfile=logging.getLogger("logmain")
            self.logfile.info("PID %s" % os.getpid())
    
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

    def put_files(self,local_file,remote_file):
        try:
            #Could use SFTP
            #self.ftp=self.ssh.open_sftp()
            #self.ftp.put(local_file,remote_file)
            self.scp=scp.SCPClient(self.ssh.get_transport())
            self.scp.put(local_file, remote_path=remote_file)
            self.logfile.info("Successfully moved file %s to %s" % (local_file,remote_file))
            return True
        except Exception,e:
            self.logfile.error("put_files caught exception %s - %s" % (e.__class__,e))
            return False
            #sys.exit(os.errno.ENOENT)
        finally:
            self.logfile.info("Closing put_files")
            #self.ftp.close()
            self.scp.close()

    def get_files(self,remote_file,local_file):
        try:
            #Could use SFTP
            #self.ftp=self.ssh.open_sftp()
            #self.ftp.get(remote_file,local_file)
            self.scp=scp.SCPClient(self.ssh.get_transport())
            self.scp.get(remote_file, local_path=local_file)
            self.logfile.info("Successfully received file from %s to %s" % (remote_file,local_file))
            return True
        except Exception,e:
            self.logfile.error("get_files caught exception %s - %s" % (e.__class__,e))
            return False
            #sys.exit(os.errno.ENOENT)
        finally:
            self.logfile.info("Closing get_files")
            #self.ftp.close()
            self.scp.close()

    def put_dirs(self,local_dir,remote_dir):
        try:
            self.scp=scp.SCPClient(self.ssh.get_transport())
            self.scp.put(local_dir, remote_path=remote_dir,recursive=True)
            #SCPClient cant control permissions on copy from Windows to Linux
            time.sleep(2)
            self.ssh.exec_command("chmod -R 755 " + remote_dir)
            self.logfile.info("Successfully put directory to %s" % (remote_dir))
            return True
        except Exception,e:
            self.logfile.error("put_dirs caught exception %s - %s" % (e.__class__,e))
            return False
        finally:
            self.logfile.info("CLOSING put_dirs")
            self.scp.close()

    def get_dirs(self,remote_dir,local_dir):
        try:
            self.scp=scp.SCPClient(self.ssh.get_transport())
            self.scp.get(remote_dir, local_path=local_dir,recursive=True)
            self.logfile.info("Successfully received directory %s" % (local_dir))
            return True
        except Exception,e:
            self.logfile.error("get_dirs caught exception %s - %s" % (e.__class__,e))
            return False
        finally:
            self.logfile.info("Closing get_dirs")
            self.scp.close()

    def done(self):
        self.ssh.close()
        self.logfile.info("Closed connection with device %s " % self.ip)



