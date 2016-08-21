#!/usr/bin/python

import sys
import socket
import os, os.path
import time

import pibrella

SOCKFILE = "/run/hat-server"

TIME_ON = 0.2
TIME_OFF = 0.2
FADE_ON = 0.2
FADE_OFF = 0.2

ts_start = 0

# -------------------------------------------------------------------------------------

def boot_start():
    pibrella.light.red.blink(TIME_ON, TIME_OFF)

# -------------------------------------------------------------------------------------

def boot_end():
    pibrella.light.red.off()
    pibrella.light.green.on()
    
# -------------------------------------------------------------------------------------

def action_start():
    pibrella.light.green.off()
    pibrella.light.yellow.pulse(FADE_ON, FADE_OFF, TIME_ON, TIME_OFF)

# -------------------------------------------------------------------------------------

def action_end():
    pibrella.light.green.on()
    pibrella.light.yellow.off()

# -------------------------------------------------------------------------------------

def halt_start():
    pibrella.light.red.blink(TIME_ON, TIME_OFF)
    pibrella.light.green.off()
    pibrella.light.yellow.off()

# -------------------------------------------------------------------------------------

def halt_end():
    pibrella.light.red.off()

# -------------------------------------------------------------------------------------

def btn_pressed(pin):
    global ts_start
    ts_start = time.time()
    print "button pressed ..."
    
# -------------------------------------------------------------------------------------

def btn_released(pin):
    global ts_start
    ts_end = time.time()
    print "button released ..."
    print "ts_start:", ts_start
    print "duration:", ts_end-ts_start
    if ts_end - ts_start > 2:
        pibrella.buzzer.success()
        os.system("halt -p &")
    else:
        pibrella.buzzer.fail()
    ts_start = 0
    
# -------------------------------------------------------------------------------------

def run_server():
    if os.path.exists(SOCKFILE):
        os.remove(SOCKFILE)      
    print "Opening socket..."
      
    server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
    server.bind(SOCKFILE)
    server.listen(5)
      
    print "Listening..."
    while True:
        conn, addr = server.accept()
        print 'accepted connection'            
        while True: 
            data = conn.recv(2)
            if not data:
                break
            elif data == "BS":
                boot_start()
            elif data == "BE":
                boot_end()
            elif data == "AS":
                action_start()
            elif data == "AE":
                action_end()
            elif data == "HS":
                halt_start()
            elif data == "HE":
                halt_end()
                print "Shutting down..."
                server.close()
                os.remove(SOCKFILE)
                return

# -------------------------------------------------------------------------------------

pibrella.button.pressed(btn_pressed)
pibrella.button.released(btn_released)
run_server()
