#!/bin/sh

kill $(pgrep -f 'python3 dataSyncherV2RawAllSensors.py')
sleep 1
python3 dataSyncherV2RawAllSensors.py &




