


import sys
import yaml
import os
import time
import glob
import shutil

from datetime import date, timedelta, datetime
mintsDefinitions         = yaml.load(open("mintsDefinitions.yaml"), Loader=yaml.SafeLoader)
print(mintsDefinitions)

nodeIDs                = mintsDefinitions['nodeIDs']



dataFolder             = mintsDefinitions['dataFolder']
dataFolderMqtt         = mintsDefinitions['dataFolderMqtt']
sensorIDs              = mintsDefinitions['sensorIDs']

print()
print("MINTS")
print()
 
startDate = datetime.strptime(mintsDefinitions['startDate'], '%Y_%m_%d')
endDate = datetime.strptime(mintsDefinitions['endDate'], '%Y_%m_%d')

delta      = timedelta(days=1)

def deleteEmptyFolders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            current_dir = os.path.join(root, dir_name)
            print("=============")
            print(current_dir)
            if not any(os.path.isfile(os.path.join(current_dir, file)) for file in os.listdir(current_dir)):
                print(f"Deleting folder: {current_dir}")
                try:
                    shutil.rmtree(current_dir)
                    print(f"Successfully deleted: {current_dir}")
                except Exception as e:
                    print(f"Error deleting {current_dir}: {e}")

def deleteFoldersWithOnlyDsStore(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            current_dir = os.path.join(root, dir_name)
            if all(file == '.DS_Store' for file in os.listdir(current_dir)):
                print(f"Deleting folder with only .DS_Store files: {current_dir}")
                try:
                    shutil.rmtree(current_dir)
                    print(f"Successfully deleted: {current_dir}")
                except Exception as e:
                    print(f"Error deleting {current_dir}: {e}")

if __name__ == "__main__":
    
    for nodeID in nodeIDs:
    
        print("========================NODES========================")
        print("Syncing node data for node "+ nodeID)
        currentDate = startDate
        includeStatements = " "
        
        while currentDate <= endDate:
            print("========================DATES========================")
            currentDateStr = currentDate.strftime("%Y_%m_%d")
            currentDate   += delta

            for sensorID in sensorIDs:
                print("========================SENSORS========================")
                print("Syncing data from node " + nodeID + ", sensor ID " + sensorID +  " for the date of " + currentDateStr)
                includeStatement = "--include='*"+  sensorID + "_" + currentDateStr +".csv' "
                includeStatements = includeStatements + includeStatement;
                    
        sysStr = 'rsync -avzrtum -e "ssh -p 2222" ' +  includeStatements+ "--include='*/' --exclude='*' mints@mintsdata.utdallas.edu:/mfs/io/groups/lary/mintsData/rawMQTT/" + nodeID + " " + dataFolderMqtt
        print(sysStr)
        os.system(sysStr)

        sysStr = 'rsync -avzrtum -e "ssh -p 2222" ' +  includeStatements+ "--include='*/' --exclude='*' mints@mintsdata.utdallas.edu:/mfs/io/groups/lary/mintsData/rawMqtt/" + nodeID + " " + dataFolderMqtt
        print(sysStr)
        os.system(sysStr)