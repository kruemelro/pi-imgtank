#!/usr/bin/python3

import sys
import socket
import os, os.path
import time

SOCKFILE = "/run/hat-server"

# -------------------------------------------------------------------------------------

if len(sys.argv) == 1:
    sys.exit(3)
else:
    # we might  be called very early during boot from udev-rules and the hat-server might
    # not be up. This will wait 10s for SOCKFILE - more than enough for a Raspberry Pi
    for _ in range(100):
        if os.path.exists(SOCKFILE):
            break
        else:
            time.sleep(0.1)
    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    sock.connect(SOCKFILE)
    #sock.sendall(sys.argv[1])
    sock.sendall(sys.argv[1].encode())
