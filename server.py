#!/usr/local/bin/python3

#
#   Wayne E. Beech
#
#   Sample server to demonstrate client/server programs and UNIX Daemons
#

#   Allow easy changing of default locations/filenames/port

port = 9020
workdir = "/tmp"
logfile = workdir + "/server.log"

#   Import the various Python libraries we need

import os
import sys
import signal
import time
import datetime
import socket
import re

#   function that is called when server receives a signal.  This
#   function logs the signal it got, the date and time the signal
#   was received, closes the socket it is listening on, closes the
#   log file and then terminates the servers

def sigterm(signum,frame):

    dt = get_dt()

    log.write("==========\n")
    log.write("%s: got signal %d, terminating\n" % (dt,signum))
    log.close();
    exit()

#   function to get the current date and time in desired format

def get_dt():

    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return dt

#   function that will process connections from clients
#   which consists or reading information from the socket
#   and writing it to a log file

def processConnection():

    try:
        data = conn.recv(512).decode()
    except:
        data = None

    while data:

        data = str(data)

        log.write("    " + data)
        log.flush()

        try:
            data = conn.recv(512).decode()
        except:
            break

    log.write("==========\n")
    log.flush()

    conn.close()

    return

#   things we need to do to be a well behaved UNIX/Linux daemon

#   fork so that we disassociate ourself from the controlling terminal 
#   and removes us from the process group that initiated the program

pid = os.fork()
if pid != 0:    # if I am the parent exit
    exit()

#   turn this program into a session leader, group leader, and
#   ensure that we do not have a controlling terminal

os.setsid()

#   change working directory to something reasonible

os.chdir(workdir)

#   set umask

os.umask(0x077)

#   close unneeded file handles
#
#   You may want to comment out the closing of stdout and
#   stderr when debugging


sys.stdin.close()
#sys.stdout.close()
#sys.stderr.close()

#   open a log file

log = open(logfile,"a")

#   end of well behaved UNIX/Linux daemon code

#   tell program how to deal with various signals it may receive.  in 
#   this case, call sigterm which will gracefully shut down the server

signal.signal(signal.SIGHUP,sigterm)
signal.signal(signal.SIGINT,sigterm)
signal.signal(signal.SIGQUIT,sigterm)
signal.signal(signal.SIGILL,sigterm)
signal.signal(signal.SIGTRAP,sigterm)
signal.signal(signal.SIGIOT,sigterm)
signal.signal(signal.SIGEMT,sigterm)
signal.signal(signal.SIGFPE,sigterm)
signal.signal(signal.SIGBUS,sigterm)
signal.signal(signal.SIGSEGV,sigterm)
signal.signal(signal.SIGSYS,sigterm)
signal.signal(signal.SIGPIPE,sigterm)
signal.signal(signal.SIGALRM,sigterm)
signal.signal(signal.SIGTERM,sigterm)
signal.signal(signal.SIGURG,sigterm)


#   get the host name of this machine and the date/time and log
#   them to the log file

hn = socket.getfqdn()

dt = get_dt()

#   set up and listen on socket

#   Create a TCP/IP socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#   Bind the socket to the port

server_address = ('localhost', port)

try:
    sock.bind(server_address)

except OSError as err:
    if re.search("Errno 48",format(err)):
        print("\nServer is already running, exiting...\n")
        quit()
    else:
        print("Unexpected error on bind")
        print(err)
        quit()

#   put a header in the log file for new server start

log.write("==========================================================\n")
log.write("%s: Server started on %s\n" % (dt,hn))
log.write("==========\n")
log.flush()

# Listen for incoming connections

sock.listen(2)

#   Process connections forever, or at least until a signal is
#   sent to the server

while True:

   conn, addr = sock.accept()
   dt = get_dt()
   log.write("%s: Accepted connection from %s\n" % (dt,addr))
   log.flush()

   processConnection()

