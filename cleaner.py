import datetime
import subprocess
import time

while True:
    now = datetime.datetime.now()
    if now.minute == 1 and now.second == 0 and now.hour % 5 == 0:
        subprocess.run(['docker-compose', 'kill'])
        subprocess.run(['docker', 'system', 'prune', '-f'])
        subprocess.run(['docker-compose', 'up', '-d'])
    time.sleep(1)
