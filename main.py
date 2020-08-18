#!/usr/bin/python
# Runs with `python main.py`
import os
import glob
import json
from csv import writer
import codecs
import re

#######################
### SET VALUES HERE ###
#######################
# KEYWORD = "start"                           # Keyword to extract data from
# MULTIPLIER = 100                            # Sets the multiplier. will only be used if the value is a float
# Will convert to int after multiplyer.
EXPORT_FILENAME = True  # Will export the CSV including the file name, ie "cover.json"
FILE_LOCATION = "./input/*.json"  # Path of JSON files relative to this file
#OUTPUT_FILE = "./output.csv"  # Location and name of the output file


#######################
### /SET VALUES HERE ##
#######################

# Functions to sort values properly with page#
def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]

def jsonparser(KEYWORD,MULTIPLIER,OUTPUT_FILE):
    # Get the names of the files
    # And sort them
    files = glob.glob(FILE_LOCATION)
    # sort by filename
    files.sort(key=natural_keys)

    # Initialize the storage
    KEYWORD_ARR = []
    max_length = 0
    if len(files) == 0:
        print("No files in input folder")
        return
    # Open each file, extract the data, conditions if necessary, and stores it in an array
    for file in files:
        FILE_ARR = []
        if EXPORT_FILENAME:
            FILE_ARR.append(os.path.basename(file))
        data = json.load(codecs.open(file, 'r', 'utf-8-sig'))
        for segment in data['segments']:
            for word in segment['words']:
                try:
                    keyword = word[KEYWORD]
                    if isinstance(keyword, float):
                        keyword = int(keyword * MULTIPLIER)  # converts float to int and multiplies by 100
                    if keyword:
                        FILE_ARR.append(keyword)
                        # print(keyword)
                except:
                    print(segment)

        if len(FILE_ARR) > max_length:
            max_length = len(FILE_ARR)
        KEYWORD_ARR.append(FILE_ARR)

    # Manually rotate the array rows => cols
    ROTATE_ARR = [["" for x in range(len(files))] for y in range(max_length)]
    colI = 0
    for row in KEYWORD_ARR:
        rowI = 0
        for rowVal in row:
            # print('{},{}: {}'.format(colI, rowI, rowVal))  # debug
            ROTATE_ARR[rowI][colI] = rowVal
            rowI += 1
        colI += 1

    # Output the file
    wtr = writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
    for x in ROTATE_ARR: wtr.writerows([x])

def main_interface():
    print("Hello Mr. Hatten. ")
    KEYWORD = input("Enter keyword: ")
    FILE_NAME = input("Enter output file name: ")
    OUTPUT_FILE = "./"+FILE_NAME+".csv"
    try:
        MULTIPLIER = int(input("Enter multiplier: "))
        jsonparser(KEYWORD,MULTIPLIER,OUTPUT_FILE)
    except ValueError:
        print("Please enter an integer. Try again.")





main_interface()