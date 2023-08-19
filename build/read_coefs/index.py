from glob import glob
import os
from os import listdir
from os.path import isfile, join
import time
import datetime
from read_image import *

def getIndexByTime(initial, time):
    if initial.minute % 2 == 0:

        startTimeInitial = initial.replace(second=30)

        if time.minute % 2 == 0:
            return int((time - startTimeInitial).total_seconds() / 60) / 2
        else:
            startTime = time - datetime.timedelta(minutes=1)
            return int((startTime - startTimeInitial).total_seconds() / 60) / 2

    else:

        startTimeInitial = initial - datetime.timedelta(minutes=1)
        startTimeInitial = startTimeInitial.replace(second=30)

        if time.minute % 2 == 0:
            return int((time - startTimeInitial).total_seconds() / 60) / 2
        else:
            startTime = time - datetime.timedelta(minutes=1)
            return int((startTime - startTimeInitial).total_seconds() / 60) / 2

initialTime = datetime.datetime.strptime("2023-07-17-11-06-40", '%Y-%m-%d-%H-%M-%S')
        
while True:
    current_index = int(getIndexByTime(initialTime, datetime.datetime.now()))
    scp = sorted(next(os.walk('../scp/'))[1])
    # scp = [s for s in scp if 0 <= int(s) <= 1500]
    print(scp)
    for i, race in enumerate(scp):
        if int(race) > 1:
            print(race)
            try:
                coefs = [f for f in listdir(f'../scp/{race}/') if isfile(join(f'../scp/{race}/', f)) and f.split(".")[1] == "jpg"]
            except:
                coefs = []
            if not len(coefs) == 0:
                for capture_path in coefs:
                    try:
                        with open(f'../scp/{race}/text.txt') as f:
                            lines = f.readlines()
                        coefs_in_lines = list(filter(lambda line: line.__contains__("coefs"), lines))
                        if not len(coefs_in_lines) >= len(coefs):
                            read_image(race, capture_path)
                    except Exception as e:
                        print(e)
                        read_image(race, capture_path)

        scp = sorted(next(os.walk('../scp/'))[1])
    time.sleep(10)
