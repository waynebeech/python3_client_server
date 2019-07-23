#!/usr/local/bin/python3

#   Things that we might need to change

serverhost = 'localhost'
port = 9020

import os
import sys
import subprocess
import socket
import string
import time

#sys.stdin.close()
#sys.stdout.close()
#sys.stderr.close()

def sendline(line):

    msg = line + "\n"

    bstr= bytes(msg, 'utf-8')

    socket.sendall(bstr)



#    get userid

output = subprocess.run('whoami',shell=1, stdout=subprocess.PIPE)

ooo = output.stdout
who = ooo.decode()
who = who.rstrip()

#   connect to server

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((serverhost, port))

# send information to server

i = 1

print("\nEnter up to 10 lines('.' to quit):\n\n")

while i < 11:

    print(str(i) + ": " , end = '')

    line = input()
    line.rstrip()

    if line == '.':
        break

    sendline(line)

    i += 1



