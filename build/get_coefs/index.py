import paramiko
from scp import SCPClient
import os
from os import listdir
from os.path import isfile, join
import time
import shutil
import datetime

def moveAll(source_folder, destination_folder):
    files = os.listdir(source_folder)

    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        
        shutil.move(source_path, destination_path)

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient('51.38.145.28', 56777, 'root', '!QAZ2wsx')
scp = SCPClient(ssh.get_transport())

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

initialTime = datetime.datetime.strptime("2023-05-12-12-20-16", '%Y-%m-%d-%H-%M-%S')
print(int(getIndexByTime(initialTime, datetime.datetime.now())))

while True:
    current_index = int(getIndexByTime(initialTime, datetime.datetime.now()))
    for i in range(current_index - 50, current_index + 10):
        if i > 1:
            print(i)
            my_coefs = []
            if os.path.exists(f'../scp/{i}'):
                my_coefs = [f for f in listdir(f'../scp/{i}') if isfile(join(f'../scp/{i}', f)) and f.split(".")[1] == "jpg"]
            if len(my_coefs) == 0:
                try:
                    if datetime.datetime.now().minute % 2 == 0:
                        scp.get(f'/!web/fortuna-ai/races/{i}/coefs/', f'../scp/{i}/', recursive=True)
                        moveAll(f'../scp/{i}/coefs', f'../scp/{i}/')
                except Exception as e:
                    print(e)
            else:
                print("already")

    time.sleep(1)
