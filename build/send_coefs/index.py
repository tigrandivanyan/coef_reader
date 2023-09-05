import paramiko
from scp import SCPClient
import os
from os import listdir
from os.path import isfile, join
import time

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

# ssh = createSSHClient('191.101.2.163', 22, 'root', '$Mayisi911')
ssh = createSSHClient('51.38.145.28', 56777, 'root', '!QAZ2wsx')
scp = SCPClient(ssh.get_transport())

while True:
    my_races = sorted(next(os.walk('../scp/'))[1])
    for race in my_races:
        print(race)
        done = [f for f in listdir(f'../scp/{race}/') if isfile(join(f'../scp/{race}/', f)) and f.split(".")[1] == "txt"]
        imgs = [f for f in listdir(f'../scp/{race}/') if isfile(join(f'../scp/{race}/', f)) and f.split(".")[1] == "jpg"]
        print(done)
        try:
            with open(f'../scp/{race}/text.txt') as f:
                lines = f.readlines()
            
            done_lines = ''

            try:
                with open(f'../scp/{race}/done.txt') as f:
                    done_lines = f.readlines()
            except:
                print('no done.txt')


            coefs_in_lines = list(filter(lambda line: line.__contains__("coefs"), lines))
            if len(coefs_in_lines) >= len(imgs) or not ''.join(lines) == ''.join(done_lines):
                try:
                    scp.put(f'../scp/{race}/text.txt', recursive=True, remote_path=f'/!web/fortuna-ai/races/{race}/coefs/')
                    try:
                        os.unlink(f'../scp/{race}/done.txt')
                    except:
                        print('no done.txt')
                    with open(f'../scp/{race}/done.txt', 'a') as the_file:
                        the_file.write(''.join(lines))
                except Exception as e:
                    print(e)
            else:
                print('still reading image')
        except:
            print("No text.txt")
    time.sleep(1)
