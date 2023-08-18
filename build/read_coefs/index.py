from glob import glob
import easyocr
import os
from os import listdir
from os.path import isfile, join
import cv2
import time
import datetime
import numpy as np
reader = easyocr.Reader(['en'], gpu = True)

def check(name):
    if(not os.path.exists(name)):
        path = os.path.join(name)
        os.mkdir(path)

# final
def coefCrop(capture, no):
    if no == "1":
        return capture[429:487, 458:574]
    elif no == "2":
        return capture[437:479, 709:809]
    elif no == "3":
        return capture[439:480, 944:1043]
    elif no == "4":
        return capture[442:480, 1181:1282]
    elif no == "5":
        return capture[442:480, 1415:1519]
    elif no == "6":
        return capture[435:481, 1647:1759]
    else:
        return capture
    
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
                            try:
                                capture = cv2.imread(f'../scp/{race}/{capture_path}')
                                coefText = ''
                                check('../tmp/')
                                for i in range(1, 7):
                                    cv2.imwrite(f'../tmp/{i}.jpg', coefCrop(capture, str(i)))

                                img_fns = sorted(glob('../tmp/*'))
                                for img in img_fns:
                                    coefText+=":"
                                    image = cv2.imread(img)
                                    average_bgr = np.mean(image[23:83, 76:186], axis=(0, 1))
                                    if average_bgr[0]*1.5 < average_bgr[2] and average_bgr[1]*1.5 < average_bgr[2]:
                                        coefText += "1,5"
                                    else:
                                        try:
                                            coefText += reader.readtext(img)[0][1]
                                        except:
                                            print('err')
                                print(coefText)
                                with open(f'../scp/{race}/text.txt', 'a') as the_file:
                                    the_file.write(f'coefs&{coefText}\n')
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                        try:
                            capture = cv2.imread(f'../scp/{race}/{capture_path}')
                            coefText = ''
                            check('../tmp/')
                            for i in range(1, 7):
                                cv2.imwrite(f'../tmp/{i}.jpg', coefCrop(capture, str(i)))

                            img_fns = sorted(glob('../tmp/*'))
                            for img in img_fns:
                                print(img)
                                coefText += ':'
                                image = cv2.imread(img)
                                average_bgr = np.mean(image[23:83, 76:186], axis=(0, 1))
                                if average_bgr[0]*1.5 < average_bgr[2] and average_bgr[1]*1.5 < average_bgr[2]:
                                    coefText += "1,5"
                                else:
                                    try:
                                        coefText += reader.readtext(img)[0][1]
                                    except:
                                        print('err')
                            print(coefText)
                            with open(f'../scp/{race}/text.txt', 'a') as the_file:
                                the_file.write(f'coefs&{coefText}\n')
                        except Exception as e:
                            print(e)
        

        scp = sorted(next(os.walk('../scp/'))[1])
    time.sleep(10)
