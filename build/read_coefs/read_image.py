from glob import glob
import easyocr
import os
import cv2
import numpy as np
reader = easyocr.Reader(['en'], gpu = True)


def coefCrop(capture, no, index):
    if index == 0:
        if no == "1":
            return capture[430:506, 451:600]
        elif no == "2":
            return capture[432:503, 682:840]
        elif no == "3":
            return capture[433:499, 922:1082]
        elif no == "4":
            return capture[433:499, 1153:1315]
        elif no == "5":
            return capture[434:498, 1381:1557]
        elif no == "6":
            return capture[433:497, 1620:1789]
        else:
            return capture
    if index == 1:
        if no == "1":
            return capture[760:826, 451:600]
        elif no == "2":
            return capture[762:823, 682:840]
        elif no == "3":
            return capture[763:829, 922:1082]
        elif no == "4":
            return capture[763:829, 1153:1315]
        elif no == "5":
            return capture[764:828, 1381:1557]
        elif no == "6":
            return capture[763:827, 1620:1789]
        else:
            return capture
    if index == 2:
        if no == "1":
            return capture[1070:1136, 451:600]
        elif no == "2":
            return capture[1072:1133, 682:840]
        elif no == "3":
            return capture[1073:1139, 922:1082]
        elif no == "4":
            return capture[1073:1139, 1153:1315]
        elif no == "5":
            return capture[1074:1138, 1381:1557]
        elif no == "6":
            return capture[1073:1137, 1620:1789]
        else:
            return capture
        
def read_coefik(img, divider, capture, indexik, small_image_index, blur):
    cv2.imwrite(f'../tmp/{small_image_index + 1}.jpg', coefCrop(capture, str(small_image_index + 1), indexik))
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
    print(divider, img)
    cv2.imwrite(img, coef_crop)


    return reader.readtext(img)[0][1]

    
def check(name):
    if(not os.path.exists(name)):
        path = os.path.join(name)
        os.mkdir(path)

def read_image(race, capture_path, indexik):
    try:
        capture = cv2.imread(f'../scp/{race}/{capture_path}')
        coefText = ''
        check('../tmp/')
        for i in range(1, 7):
            cv2.imwrite(f'../tmp/{i}.jpg', coefCrop(capture, str(i), indexik))

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
            elif(average_green > average_blue and average_green > average_red):
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

        for index, img in enumerate(img_fns):
            coefText+=":"

            if index == highest:
                coefText+="H"
            elif index == lowest:
                coefText+="L"
            else:
                print('0')
                coefik_text = read_coefik(img, 2, capture, indexik, index, True)
                if not ',' in coefik_text and not '.' in coefik_text:
                    print('1')
                    coefik_text = read_coefik(img, 2.5, capture, indexik, index, True)
                    if not ',' in coefik_text and not '.' in coefik_text:
                        print('3')
                        coefik_text = read_coefik(img, 3, capture, indexik, index, True)
                        if not ',' in coefik_text and not '.' in coefik_text:
                            print('4')
                            coefik_text = read_coefik(img, 2, capture, indexik, index, False)
                            if not ',' in coefik_text and not '.' in coefik_text:
                                print('5')
                                coefik_text = read_coefik(img, 2.5, capture, indexik, index, False)
                                if not ',' in coefik_text and not '.' in coefik_text:
                                    print('6')
                                    coefik_text = read_coefik(img, 3, capture, indexik, index, False)

                try:
                    coefText += coefik_text
                except:
                    print('err')

        print(coefText)
        with open(f'../scp/{race}/text.txt', 'a') as the_file:
            if indexik == 0:
                the_file.write(f'coefs&{coefText}\n')
            if indexik == 1:
                the_file.write(f'coefs_mid&{coefText}\n')
            if indexik == 2:
                the_file.write(f'coefs_last&{coefText}\n')
    except Exception as e:
        print(e)