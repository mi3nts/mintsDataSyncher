# Mints Data Syncher
The data collected on Mints network can be dowloaded to your pc using this repo.

## For a limited amount of nodes, sensors, and time spans.
1. Contact a member of the Mints team to provide your SSH public key.
2. Copy the file mintsDefinitions.txt and save it as mintsDefinitions.yaml.
3. Edit mintsDefinitions.yaml to reflect the time span, node IDs and the sensor IDs you want to download.
4. Further adjust the destination folder's date to match your desired data location.
5. Run `python3 dataSyncherV2RawFiltered.py` to sync data from the rsync pipeline.
6. Execute `python3 dataSyncherV2RawMqttFiltered.py` to sync data from the MQTT pipeline (Note: All LoRaWAN data is exclusively collected via rsync).

## For a complete set of nodes
1. Contact a member of the Mints team to provide your SSH public key.
2. Copy the file mintsDefinitions.txt and save it as mintsDefinitions.yaml.
4. Adjust the destination folder's date to match your desired data location.
5. Run `python3 dataSyncherV2Raw.py` to sync data from the rsync pipeline.
6. Execute `python3 dataSyncherV2RawMqtt.py` to sync data from the MQTT pipeline (Note: All LoRaWAN data is exclusively collected via rsync).
