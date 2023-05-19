# Import tkinter and webview libraries
from fileinput import filename
from tkinter import *
from traceback import print_stack
# import webview
import glob
import serial
import datetime
# from mintsXU4 import mintsSensorReader as mSR
# from mintsXU4 import mintsDefinitions as mD
import time
# import serial
# import pynmea2
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
import mintsLatest as mL
import csv
import os 
# import nmap, socket
import yaml
import json




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
latestFolder       = dataFolder+ "/latest"
print()
print("MINTS")
print()
 
startDate = datetime.strptime(mintsDefinitions['startDate'], '%Y_%m_%d')
endDate   = datetime.strptime(mintsDefinitions['endDate'], '%Y_%m_%d')

delta      = timedelta(days=1)

def directoryCheckV2(outputPath):
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


def readLatestTime(hostID,sensorID):
    fileName = latestFolder + "/" + hostID+"_"+sensorID+".json"
    if os.path.isfile(fileName):
        try:    
            with open(fileName, 'r') as f:
                data = json.load(f)
            return datetime.strptime(data['dateTime'],'%Y-%m-%d %H:%M:%S.%f')

        except Exception as e:
            
            print(e)
    else:
        return datetime.strptime("2022-10-04 22:40:40.204179",'%Y-%m-%d %H:%M:%S.%f')
   
def writeLatestTime(hostID,sensorID,dateTime):
    fileName = latestFolder + "/" + hostID+"_"+sensorID+".json"
    directoryCheckV2(fileName)
    sensorDictionary = OrderedDict([
                ("dateTime"            ,str(dateTime))
                ])
    with open(fileName, "w") as outfile:
        json.dump(sensorDictionary,outfile)



# Basic Needs - When given a Node ID 
# and a set of sensor IDs 
# get a list of CSVs and Update via MQTT 
# Keep a record of last time stamp sent for each nodes each sensor ID
# Get a list of
def syncDataViaMQTT(nodeID,sensorID):
    csvDataFiles = glob.glob(dataFolder + "/raw/" + nodeID + "/*/*/*/*"+sensorID+"*.csv")
    csvDataFiles.sort()
    print(csvDataFiles)
    for csvFile in csvDataFiles:
        print("================================================")
        print("File Name")
        print(csvFile)
        # try:
        with open(csvFile, "r") as f:
            sensorID          = csvFile.split("_")[-4]
            reader            = csv.DictReader((line.replace('\0','') for line in f) )
            rowList           = list(reader)
            latestDateTime    = readLatestTime(nodeID,sensorID)
            csvLatestDateTime = datetime.strptime(rowList[-1]['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
                        
            if csvLatestDateTime > latestDateTime:
                for rowData in rowList:
                    # try:
                        dateTimeRow = datetime.strptime(rowData['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
                        if dateTimeRow > latestDateTime:
                            print("Publishing MQTT Data ==> Node ID:"+nodeID+ ", Sensor ID:"+ sensorID+ ", Time stamp: "+ str(dateTimeRow))
                            mL.writeMQTTLatestWearable(nodeID,sensorID,rowData)  
                            time.sleep(0.001)
                                            
                        # except Exception as e:
                        #     print(e)
                        #     print("Data row not published")

                writeLatestTime(nodeID,sensorID,csvLatestDateTime)
                print("================================================")
                print("Latest Date Time ==> Node:"+ nodeID + ", SensorID:"+ sensorID)
                print(csvLatestDateTime)
                print("================================================")

        # except Exception as e:
        #     print(e)
        #     print("Data file not published")
        #     print(csvFile)
        
        time.sleep(1)
        dateTime = datetime.now() 

def main():
    for nodeID in nodeIDs:
        print("========================NODES========================")
        for sensorID in sensorIDs:
            print("Sending MQTT data for " + nodeID + "/"+ sensorID) 
            syncDataViaMQTT(nodeID,sensorID)




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()