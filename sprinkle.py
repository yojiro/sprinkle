#!/usr/bin/env python2.7

# simple utility for garden sprinkler
# (C) 2013 Yojiro UO <yuo@nui.org>, All right reserved.


import RPi.GPIO as GPIO
from ConfigParser import ConfigParser
import logging
from logging.handlers import SysLogHandler
import os
import sys
import signal
from time import sleep
import threading
from optparse import OptionParser

SW_PORT    = 23
LED_PORT   = 24
WATER_PORT = 25

class water(threading.Thread):
    def __init__(self, min):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sec = min * 60

    def run(self):
        logger.info("sprinkler start:%d sec" % self.sec)
        GPIO.output(WATER_PORT, True)
        while (self.sec > 0):
            sleep(10)
            self.sec -= 10 
            if (self.sec % 30 == 0):
                logger.debug('(remain: %d sec)', self.sec )
        else:
            GPIO.output(WATER_PORT, False)
            logger.info("sprinkler finish")

def sw_cb(ch):
    logger.info("key pressed: %s" % ch)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SW_PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Switch
    GPIO.setup(LED_PORT, GPIO.OUT, initial=GPIO.HIGH) # LED
    GPIO.setup(WATER_PORT, GPIO.OUT, initial=GPIO.LOW) # water
    GPIO.add_event_detect(SW_PORT, GPIO.RISING)

def close_gpio():
    GPIO.remove_event_detect(SW_PORT)
    GPIO.cleanup()

def signal_handler(signal, frame):
    close_gpio()
    sys.exit(0)

if __name__ == "__main__":
    # parser config
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", action="store_true", dest='debug',
            default=False, help="debug output")
    parser.add_option("-t", "--time", dest="stime", 
            action="store", type="int",
            default=30, help="sprinkle time (min)")

    (options, args) = parser.parse_args()

    # logging config
    loglevel = logging.INFO
    if options.debug:
        loglevel = logging.DEBUG

    logger=logging.getLogger()
    logger.setLevel(loglevel)
    syslog = SysLogHandler(address='/dev/log')
    formatter = logging.Formatter(
            fmt='(%(name)s %(levelname)-8s %(message)s')
    syslog.setFormatter(formatter)
    logger.addHandler(syslog)

    # GPIO setting
    init_gpio()
    GPIO.add_event_callback(SW_PORT, sw_cb, bouncetime=200)

    # signal handler
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        t = water(options.stime)
        t.start()
        sleep(5)
        t.join()
    except KeyboardInterrupt:
        logger.info("ctrl-c pressed ... exit")
        GPIO.output(LED_PORT, False)
        close_gpio()
        sys.exit(1)
    except:
        close_gpio()
        logger.info("stopped")
        sys.exit(1)
