import sys
import yaml
import os
import time
import glob
import shutil
import pandas as pd
from datetime import datetime


# Load YAML configuration
with open("mintsDefinitions.yaml") as f:
    mintsDefinitions = yaml.safe_load(f)

print(mintsDefinitions)

# Extract relevant parameters
nodeIDs = mintsDefinitions['nodeIDs']
dataFolder = mintsDefinitions['dataFolder']
dataFolderMqtt = mintsDefinitions['dataFolderMqtt']
sensorIDs = mintsDefinitions['sensorIDs']

print("\nMINTS\n")

# Define Node ID (modify if needed)
nodeID = "001e064a8753"

# Define path pattern
path = os.path.join(dataFolder, nodeID, "*", "*", "*", "*.csv")

print("Looking for files in:", path)

# Get list of CSV files
csv_files = sorted(glob.glob(path))  # Sorting ensures proper order

print("Files found:")
for file in csv_files:
    print(file)

# Read and concatenate all files
df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Save the merged file
output_path = "merged_output.csv"
df.to_csv(output_path, index=False)
print(f"Merged CSV saved as: {output_path}")

# Display the first few rows of the merged DataFrame
print(df.head())