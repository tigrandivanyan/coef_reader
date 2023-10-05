from glob import glob
import os
from os import listdir
from os.path import isfile, join
import datetime
import asyncio  # Import asyncio library for asynchronous tasks
from read_image import read_image  # Assuming read_image is an asynchronous function

async def process_race(race):
    print("Reading race: ", race)
    try:
        coefs = [f for f in listdir(f'../scp/{race}/') if isfile(join(f'../scp/{race}/', f)) and f.split(".")[1] == "jpg"]
    except:
        coefs = []
    if not len(coefs) == 0:
        for capture_path in coefs:
            print('Reading image', capture_path)
            try:
                with open(f'../scp/{race}/text.txt') as f:
                    lines = f.readlines()
                coefs_in_lines = list(filter(lambda line: line.__contains__("coefs&:"), lines))
                if not len(coefs_in_lines) >= len(coefs):
                    # Record the timestamp before time.sleep(1)
                    start_time = datetime.datetime.now()
                    await read_image(race, capture_path)

                    # Record the timestamp after time.sleep(1)
                    end_time = datetime.datetime.now()

                    # Calculate the time difference
                    time_difference = end_time - start_time

                    # Print the time difference
                    print("Time difference:", time_difference)
            except Exception as e:
                print(e)
                # Record the timestamp before time.sleep(1)
                start_time = datetime.datetime.now()
                await read_image(race, capture_path)

                # Record the timestamp after time.sleep(1)
                end_time = datetime.datetime.now()

                # Calculate the time difference
                time_difference = end_time - start_time

                # Print the time difference
                print("Time difference:", time_difference)

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

async def main():
    initialTime = datetime.datetime.strptime("2023-07-17-11-06-40", '%Y-%m-%d-%H-%M-%S')

    while True:
        current_index = int(getIndexByTime(initialTime, datetime.datetime.now()))
        scp = sorted(next(os.walk('../scp/'))[1])
        scp = [s for s in scp if current_index - 10 <= int(s) <= current_index + 10]
        print(scp)
        
        # Create tasks for processing races concurrently
        tasks = [process_race(race) for race in scp if int(race) > 1]
        await asyncio.gather(*tasks)  # Execute tasks concurrently

        scp = sorted(next(os.walk('../scp/'))[1])
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())  # Run the asynchronous main function
