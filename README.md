# Mints Data Syncher
The data collected on the Mints network can be downloaded to your PC using this repository.

## For a Limited Number of Nodes, Sensors, and Time Spans
1. Contact a member of the Mints team to provide your SSH public key.
2. Copy the file `mintsDefinitions.txt` and save it as `mintsDefinitions.yaml`.
3. Edit `mintsDefinitions.yaml` to specify the time span, node IDs, and sensor IDs you want to download.
4. Adjust the destination folder's date to match your desired data location.
5. Run `python3 dataSyncherV2RawFiltered.py` to sync data from the rsync pipeline.
6. Execute `python3 dataSyncherV2RawMqttFiltered.py` to sync data from the MQTT pipeline (Note: All LoRaWAN data is exclusively collected via rsync).

## For a Complete Set of Nodes
1. Contact a member of the Mints team to provide your SSH public key.
2. Copy the file `mintsDefinitions.txt` and save it as `mintsDefinitions.yaml`.
3. Adjust the destination folder's date to match your desired data location.
4. Run `python3 dataSyncherV2Raw.py` to sync data from the rsync pipeline.
5. Execute `python3 dataSyncherV2RawMqtt.py` to sync data from the MQTT pipeline (Note: All LoRaWAN data is exclusively collected via rsync).
