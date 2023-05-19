

import sys
import yaml
import os
import time
import glob

from datetime import date, timedelta, datetime
mintsDefinitions         = yaml.load(open("mintsDefinitions.yaml"))
print(mintsDefinitions)
nodeIDs            = mintsDefinitions['nodeIDs']
dataFolder         = mintsDefinitions['dataFolder']
sensorIDs          = mintsDefinitions['sensorIDs']

print()
print("MINTS")
print()
 
startDate = datetime.strptime(mintsDefinitions['startDate'], '%Y_%m_%d')
endDate = datetime.strptime(mintsDefinitions['endDate'], '%Y_%m_%d')

delta      = timedelta(days=1)



 
for nodeID in nodeIDs:
    print("========================NODES========================")
    currentDate = startDate
    while currentDate <= endDate:
        print("========================DATES========================")
        currentDateStr = currentDate.strftime("%Y_%m_%d")
        currentDate   += delta
        for sensorID in sensorIDs:
            print("========================SENSORS========================")
            print("Syncing data from node " + nodeID + ", sensor ID " + sensorID +  " for the date of " + currentDateStr)
            # print("rsync command:")
            # sysStr = 'rsync -avzrtu -e "ssh -p 2222" ' +  "--include='" +"*"+  sensorID + "_" + currentDateStr +  ".csv' --include='*/' --exclude='*' mints@mintsdata.utdallas.edu:/mfs/io/groups/lary/mintsData/raw/" + nodeID + " " + dataFolder
            # print(sysStr)
            # os.system(sysStr)
            sysStr = 'rsync -avzrtu -e "ssh -p 2222" ' +  "--include='" +"*"+  sensorID + "_" + currentDateStr +  ".csv' --include='*/' --exclude='*' mints@mintsdata.utdallas.edu:/home/mints/raw/" + nodeID + " " + dataFolder + "/raw"
            # print(sysStr)
            os.system(sysStr)
