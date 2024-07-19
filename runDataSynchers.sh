#!/bin/sh

kill $(pgrep -f 'python3 dataSyncherV2Biometrics.py')
sleep 1
python3 dataSyncherV2Biometrics.py &

kill $(pgrep -f 'python3 dataSyncherV2Calibrated.py')
sleep 1
python3 dataSyncherV2Calibrated.py &

kill $(pgrep -f 'python3 dataSyncherV2External.py')
sleep 1
python3 dataSyncherV2External.py &

kill $(pgrep -f 'dataSyncherV2LiveUpdates.py')
sleep 1
python3 dataSyncherV2LiveUpdates.py &

kill $(pgrep -f 'python3 dataSyncherV2LoRaMetaData.py')
sleep 1
python3  dataSyncherV2LoRaMetaData.py &

kill $(pgrep -f 'python3 dataSyncherV2Reference.py')
sleep 1
python3  dataSyncherV2Reference.py &

kill $(pgrep -f 'python3 dataSyncherV2RawMqtt.py')
sleep 1
python3 dataSyncherV2RawMqtt.py &

kill $(pgrep -f 'python3  dataSyncherV2Raw.py')
sleep 1
python3  dataSyncherV2Raw.py &

