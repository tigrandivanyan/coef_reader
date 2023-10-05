from glob import glob
import easyocr
import os
import cv2
import numpy as np
from coefCrop import *
import time
import datetime
import shutil
reader = easyocr.Reader(['en'], gpu = False)

def read_coefik(img, divider, capture, race, blur):
    coefCrop(capture, race)
    image = cv2.imread(img)
    indexed_image = image
    average_color = np.mean(indexed_image, axis=(0, 1))[::-1]
    red = average_color[0]
    green = average_color[1]
    blue = average_color[2]

    brightness = red + green + blue

    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define a threshold for the value channel
    brightness_threshold = brightness / 2  # Adjust this threshold value as needed

    # Create a mask to filter out dark pixels
    mask = hsv_image[:, :, 2] > brightness_threshold

    # Apply the mask to the original image
    filtered_image = image.copy()
    filtered_image[~mask] = 0

    # Calculate the average RGB values of the remaining pixels
    remaining_pixels = filtered_image[mask]
    average_red = np.mean(remaining_pixels[:, 2])
    average_green = np.mean(remaining_pixels[:, 1])
    average_blue = np.mean(remaining_pixels[:, 0])

    brightness = average_red + average_green + average_blue
    threshVale = int(brightness / divider)

    if threshVale > 200:
        threshVale = 200

    # Convert to grayscale
    coef_crop = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, coef_crop = cv2.threshold(coef_crop, threshVale, 255, cv2.THRESH_BINARY)

    # Apply Gaussian blur
    if blur:
        coef_crop = cv2.GaussianBlur(coef_crop, (5, 5), 0)

    # Apply histogram equalization for monotonicity
    coef_crop = cv2.equalizeHist(coef_crop)
    cv2.imwrite(img.split('jpg')[0] + "_" + str(divider) + "_" + str(blur) + '.jpg', coef_crop)
    # time.sleep(1)
    try:
        a3 = reader.readtext(img.split('jpg')[0] + "_" + str(divider) + "_" + str(blur) + '.jpg')
        readed_text = a3[0][1]
    except Exception as e:
        print(e)
        readed_text = ''
    return readed_text


    
def check(name):
    if(not os.path.exists(name)):
        path = os.path.join(name)
        os.mkdir(path)

async def read_image(race, capture_path):
    try:
        capture = cv2.imread(f'../scp/{race}/{capture_path}')
        coefText = ''
        try:
            shutil.rmtree('../tmp/')
        except:
            print("No tmp")
        check('../tmp/')
        coefCrop(capture, race)

        img_fns = sorted(glob('../tmp/*'))
        reds = []
        greens = []
        for index, img in enumerate(img_fns):
            image = cv2.imread(img)

            indexed_image = image
            average_color = np.mean(indexed_image, axis=(0, 1))[::-1]
            red = average_color[0]
            green = average_color[1]
            blue = average_color[2]

            brightness = red + green + blue

            # Convert to HSV color space
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Define a threshold for the value channel
            brightness_threshold = brightness / 2  # Adjust this threshold value as needed

            # Create a mask to filter out dark pixels
            mask = hsv_image[:, :, 2] > brightness_threshold

            # Apply the mask to the original image
            filtered_image = image.copy()
            filtered_image[~mask] = 0

            # Calculate the average RGB values of the remaining pixels
            remaining_pixels = filtered_image[mask]
            average_red = np.mean(remaining_pixels[:, 2])
            average_green = np.mean(remaining_pixels[:, 1])
            average_blue = np.mean(remaining_pixels[:, 0])

            if average_red > average_green * 1.4 and average_red > average_blue * 1.4:
                reds.append([index, average_red - average_green + average_red - average_blue])
            elif(average_green > average_blue * 1.1 and average_green > average_red * 1.2):
                greens.append([index, average_green - average_red + average_green - average_blue])

        maxRed = 0
        maxRedIndex = -1
        for e in reds:
            index = e[0]
            value = e[1]
            if value > maxRed:
                maxRed = value
                maxRedIndex = index
        
        lowest = maxRedIndex


        maxGreen = 0
        maxGreenIndex = -1
        for e in greens:
            index = e[0]
            value = e[1]
            if value > maxGreen:
                maxGreen = value
                maxGreenIndex = index
        
        highest = maxGreenIndex

        print(img_fns)
        for index, img in enumerate(img_fns):
            coefText+=":"

            if index == highest:
                coefText+="H"
            elif index == lowest:
                coefText+="L"
            else:
                variants = []
                print("Strating varitant addition", img)
                variants.append(read_coefik(img, 2, capture, race, True))
                variants.append(read_coefik(img, 2.5, capture, race, True))
                variants.append(read_coefik(img, 3, capture, race, True))
                variants.append(read_coefik(img, 2, capture, race, False))
                variants.append(read_coefik(img, 2.5, capture, race, False))
                variants.append(read_coefik(img, 3, capture, race, False))
                print("Finshing varitant addition", img)
                try:
                    coefText += "$$".join(variants)
                except:
                    print('err')

        print(coefText)
        with open(f'../scp/{race}/text.txt', 'a') as the_file:
            the_file.write(f'coefs&{coefText}\n')

    except Exception as e:
        print(e)