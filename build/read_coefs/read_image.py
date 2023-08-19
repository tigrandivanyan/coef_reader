from glob import glob
import easyocr
import os
import cv2
import numpy as np
reader = easyocr.Reader(['en'], gpu = True)


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
    
def check(name):
    if(not os.path.exists(name)):
        path = os.path.join(name)
        os.mkdir(path)

def read_image(race, capture_path):
    try:
        capture = cv2.imread(f'../scp/{race}/{capture_path}')
        coefText = ''
        check('../tmp/')
        for i in range(1, 7):
            cv2.imwrite(f'../tmp/{i}.jpg', coefCrop(capture, str(i)))

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
                threshVale = int(brightness / 2.3)

                if threshVale > 200:
                    threshVale = 200
                
                # Convert to grayscale
                coef_crop = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, coef_crop = cv2.threshold(coef_crop, threshVale, 255, cv2.THRESH_BINARY)

                # Apply Gaussian blur
                coef_crop = cv2.GaussianBlur(coef_crop, (5, 5), 0)

                # Apply histogram equalization for monotonicity
                coef_crop = cv2.equalizeHist(coef_crop)

                cv2.imwrite(img, coef_crop)
                try:
                    coefText += reader.readtext(img)[0][1]
                except:
                    print('err')

        print(coefText)
        with open(f'../scp/{race}/text.txt', 'a') as the_file:
            the_file.write(f'coefs&{coefText}\n')
    except Exception as e:
        print(e)