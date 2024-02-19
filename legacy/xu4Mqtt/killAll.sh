#!/bin/bash
#
sleep 1
kill $(pgrep -f 'ips7100ReaderV1.py')
sleep 2

kill $(pgrep -f 'i2cReader.py')
sleep 2

kill $(pgrep -f 'gpsReader.py')
sleep 2

kill $(pgrep -f 'batteryReader.py')
sleep 2