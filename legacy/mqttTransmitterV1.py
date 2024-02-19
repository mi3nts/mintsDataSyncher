

import sys
import yaml
import os
import time
import glob
import shutil
from datetime import date, timedelta, datetime
import csv
# from mintsXU4 import mintsLatest as mL
from collections import OrderedDict
import json


mintsDefinitions         = yaml.load(open("mintsDefinitions.yaml"))
print(mintsDefinitions)

nodeIDs            = mintsDefinitions['nodeIDs']
dataFolder         = mintsDefinitions['dataFolder']
dataFolderMqtt     = mintsDefinitions['dataFolderMqtt']
latestFolder       = mintsDefinitions['latestFolder']
sensorIDs          = mintsDefinitions['sensorIDs']



print()
print("MINTS")
print()
 
startDate = datetime.strptime(mintsDefinitions['startDate'], '%Y_%m_%d')
endDate   = datetime.strptime(mintsDefinitions['endDate'], '%Y_%m_%d')

delta     = timedelta(days=1)


import os


def readLatestTime(nodeID,sensorID):
    fileName = latestFolder + "/" + nodeID+"_"+sensorID+".json"
    if os.path.isfile(fileName):
        try:    
            with open(fileName, 'r') as f:
                data = json.load(f)
            return datetime.strptime(data['dateTime'],'%Y-%m-%d %H:%M:%S.%f')

        except Exception as e:
            
            print(e)
    else:
        return datetime.strptime("2020-01-01 00:00:00.000000",'%Y-%m-%d %H:%M:%S.%f')

def directoryCheck2(outputPath):
    isFile = os.path.isfile(outputPath)
    if isFile:
        return True
    if outputPath.find(".") > 0:
        directoryIn = os.path.dirname(outputPath)
    else:
        directoryIn = os.path.dirname(outputPath+"/")

    if not os.path.exists(directoryIn):
        print("Creating Folder @:" + directoryIn)
        os.makedirs(directoryIn)
        return False
    return True;




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

def writeLatestTime(nodeID,sensorID,dateTime):
    fileName = latestFolder + "/" + nodeID+"_"+sensorID+".json"
    directoryCheck2(fileName)
    sensorDictionary = OrderedDict([
                ("dateTime"            ,str(dateTime))
                ])
    with open(fileName, "w") as outfile:
        json.dump(sensorDictionary,outfile)

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
            print(currentDateStr)
            # Only limiting it to dates and node IDs - Not filtering sensor IDs
            # for sensorID in sensorIDs:
            #     print("========================SENSORS========================")

            print("Syncing data from node " + nodeID + " for the date of " + currentDateStr)
            # print(dataFolder)
            csvDataFiles = glob.glob(dataFolder+"/"+nodeID+ "/*/*/*/*"+ currentDateStr+"*.csv")
            csvDataFiles.sort()
            print(csvDataFiles)
            for csvFile in csvDataFiles:
                print("================================================")
                print(csvFile)
                rowList = []
                with open(csvFile, "r") as f:
                    reader = csv.DictReader(f)
                    try:
                        for row in reader:
                            # Check if some of the values in the row are null
                            if not any(value is None for value in row.values()):
                                rowList.append(row)
                    except csv.Error as e:
                        print(f"CSV Error: {e}")

                    sensorID          = csvFile.split("_")[-4]
                    latestDateTime    = readLatestTime(nodeID,sensorID)

                    try:
                        csvLatestDateTime = datetime.strptime(rowList[-1]['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
                    except Exception as e:
                        print(e)
                        print("Data row not published") 
                        continue

                    if csvLatestDateTime > latestDateTime:
                        for rowData in rowList:
                            try:
                                dateTimeRow = datetime.strptime(rowData['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
                                # print(rowData)
                                if dateTimeRow > latestDateTime:
                                    print("Publishing MQTT Data ==> Node ID:"+nodeID+ ", Sensor ID:"+ sensorID+ ", Time stamp: "+ str(dateTimeRow))
                                    writeMQTTLatestNodeID(nodeID,sensorID,rowData)  
                                    time.sleep(0.001)
                                    
                            except Exception as e:
                                print(e)
                                print("Data row not published")
                                continue

                        writeLatestTime(nodeID,sensorID,csvLatestDateTime)
                        print("================================================")
                        print("Latest Date Time ==> Node:"+ nodeID + ", SensorID:"+ sensorID)
                        print(csvLatestDateTime)
                        print("================================================")
                        # time.sleep(5)
