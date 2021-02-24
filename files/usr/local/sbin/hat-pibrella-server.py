#!/usr/bin/python3

import sys
import socket
import os, os.path
import time
import datetime
import threading

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106

from gpiozero import Button
from subprocess import check_call
from signal import pause

import psutil

#import pibrella

SOCKFILE = "/run/hat-server"

TIME_ON = 0.2
TIME_OFF = 0.2
FADE_ON = 0.2
FADE_OFF = 0.2

ts_start = 0

serial = spi(device=0, port=0)
device = sh1106(serial)

button = Button(14, pull_up=True, hold_time=3)


####### Display variables ###############

#global status
# -------------------------------------------------------------------------------------

def boot_start():
    print ("Boot Start")
    global status
    status = "booting..."
# -------------------------------------------------------------------------------------

def boot_end():
    print ("Ready")
    global status
    status = "Ready"
# -------------------------------------------------------------------------------------

def action_start():
    print ("Copy Start")
    global status
    status = "working"
    global tstart
    tstart = datetime.datetime.now()
# -------------------------------------------------------------------------------------

def action_end():
    print ("Action End")
    global status
    status = "booting..."
# -------------------------------------------------------------------------------------

def halt_start():
     print ("Shutdown Start")
     global status
     status = "shutdown"
# -------------------------------------------------------------------------------------

def halt_end():
    print ("Stutdown End")

# -------------------------------------------------------------------------------------

def shutdown():
    print ("shutdown")
    i = 3
    global status
    global shutdowntimer
    while button.is_pressed and i>0:
        shutdowntimer = i
        status = "shutdown"
        print (i)
        i=i-1
        time.sleep(1)
    if not button.is_pressed:
        status = "ready"
    else:
        print ("shutdown now")
        status = "Bye"
        os.system("umount /data")
        os.system("hdparm -Y /dev/disk/by-partuuid/cea650ab-d65f-3241-87f8-188562cdb0fc")
        os.system("halt -p &")

# -------------------------------------------------------------------------------------

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s %s' % (value, s)
    return "%sB" % n

# -------------------------------------------------------------------------------------

def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s used" % (bytes2human(usage.used))

def disk_free(dir):
    usage = psutil.disk_usage(dir)
    return "HDD:  %s left" % (bytes2human(usage.free))

# -------------------------------------------------------------------------------------

def size(path):

    #initialize the size
    total_size = 0

    #use the walk() method to navigate through directory tree
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:
            #use join to concatenate all the components of path
            f = os.path.join(dirpath, i)
            #use getsize to generate size in bytes and add it to the total size
            total_size += os.path.getsize(f)
    return total_size
# -------------------------------------------------------------------------------------

def remains(total, done):
    now  = datetime.datetime.now()
#    global tstart
#    print (tstart)
#    print (now)
#    print (total)
#    print (done)
    if done == 0:
        done = 1
    left = (total - done) * (now - tstart) / done
    sec = int(left.total_seconds())
#    if sec < 60:
#       return "{} seconds".format(sec)
#    else:
#       return "{} minutes".format(int(sec / 60))
    return str(datetime.timedelta(seconds=sec))

def print_display():
    global status
    global shutdowntimer
    while True:
        if status == 'shutdown':
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="black", fill="white")
                draw.text((20, 30), "Shutdown in..."+str(shutdowntimer), fill="black")
        elif status == 'Bye':
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="black", fill="black")
                draw.text((55, 30), "Bye", fill="white")
        else:
            #grepping values
            now = datetime.datetime.now()
            today_date = now.strftime("%d %b %y")
            today_time = now.strftime("%H:%M:%S")

            # creating display content
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.rectangle([75,0,128,11], outline="white", fill="white")
                draw.text((80, 1), today_time, fill="black")
                # Status
                draw.text((2, 2), status, fill="white")
                draw.text((2, 50), disk_free('/data/'), fill="white")

                # Copy
                if os.path.exists("/tmp/sdcard") and os.path.exists("/tmp/destination"):
                    source = size("/tmp/sdcard/")
                    destination = size("/tmp/destination/")
                    if source > 0:
                        draw.text((2,20), "ETA:  " + remains(source,destination), fill="white")
                        progress = destination / source * 100
                        draw.text((2,35), "Copy: " +'{0:.2f}'.format(progress) + " %", fill="white")
        time.sleep(.5)


def display_server():
    display_thread = threading.Thread(target=print_display, name="Display Server", daemon=True)
    display_thread.start()
# -------------------------------------------------------------------------------------

def run_server():
    if os.path.exists(SOCKFILE):
        os.remove(SOCKFILE)
    print ("Opening socket...")

    server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
    server.bind(SOCKFILE)
    server.listen(5)

    print ("Listening...")
    while True:
        conn, addr = server.accept()
        print ("accepted connection")
        while True:
            data = conn.recv(2)
#            print (data)
            if not data:
                break
            elif data == b'BS':
                boot_start()
            elif data == b'BE':
                boot_end()
            elif data == b'AS':
                action_start()
            elif data == b'AE':
                action_end()
            elif data == b'HS':
                halt_start()
            elif data == b'HE':
                halt_end()
                print ("Shutting down...")
                server.close()
                os.remove(SOCKFILE)
                return
            else:
                print ("Command not found")


# -------------------------------------------------------------------------------------
button.when_pressed = shutdown
global status
status = "Ready"
shutdowntimer = 3
display_server()
run_server()
