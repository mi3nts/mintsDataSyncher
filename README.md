# MintsDataSyncher

## Steps
1. Contact a member of the Mints team to provide your SSH public key.
2. Duplicate the file mintsDefinitions.txt and save it as mintsDefinitions.yaml.
3. Adjust the destination folder's date to match your desired data location.
4. Specify the node, sensor IDs and the desired start and end date.
5. Execute `python3 dataSyncherRaw.py` for data collected from the rsync pipeline.
6. Run `python3 dataSyncherRawMqtt.py` for data gathered from the MQTT pipeline (Note: All LoRaWAN data is exclusively collected via rsync).


