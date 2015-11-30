#!/usr/bin/python
# coding=utf-8
#
# Test-Sensor-HT-DHT.py - Read from the DHT sensor
#
# Usage:
# ./Test-Sensor-HT-DHT.py [sensor] [pin]
#
# Where sensor can be DHT11, DHT22, or AM2302
# Where pin is the GPIO (BCM numbering) connected to the sensor data pin

import os
import sys

if not os.geteuid() == 0:
    print "Error: Script must be executed as root.\n"
    sys.exit(1)

import argparse
import time

import Adafruit_DHT


def menu():
    parser = argparse.ArgumentParser(description='Read from the DHT sensor')
    parser.add_argument('sensor', choices=['DHT11', 'DHT22', 'AM2302'], help="Sensor Name")
    parser.add_argument('pin', type=int,
                        help="The GPIO (BCM numbering) connected to the sensor data pin")

    args = parser.parse_args()

    sensor, pin = args

    if sensor == 'DHT11':
        device = Adafruit_DHT.DHT11
    elif sensor == 'DHT22':
        device = Adafruit_DHT.DHT22
    elif sensor == 'AM2302':
        device = Adafruit_DHT.AM2302
    else:
        # Invalid device name
        sys.exit(1)

    if not 0 < pin < 40:
        print 'Error: Invalid GPIO pin.\n'
        sys.exit(1)

    for x in range(10):
        humidity, temperature = Adafruit_DHT.read_retry(device, pin)
        print "Temperature: %s" % temperature
        print "Humidity: %s" % humidity
        time.sleep(2)


if __name__ == "__main__":
    menu()
