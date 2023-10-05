import cv2
import numpy as np

# preset values

prev_rect_values = False
prev_race = 0
default_length_between_rects = 350
default_length_between_rects_and_nums = 85

def coefCrop(capture, race):
    crop_y = 304
    crop_y_w = 544

    crop_x = 313
    crop_x_h = 1868


    global prev_rect_values
    global prev_race
    width = crop_x_h - crop_x

    original_image = capture[crop_y:crop_y_w, crop_x:crop_x_h]
    image = capture[crop_y:crop_y_w, crop_x:crop_x_h]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []

    count = 0
    for index, contour in enumerate(contours):
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if len(approx) == 4:
            count+=1
            angles = []
            for i in range(4):
                angle = np.degrees(np.arctan2(
                    approx[(i + 1) % 4, 0, 1] - approx[i, 0, 1],
                    approx[(i + 1) % 4, 0, 0] - approx[i, 0, 0]))
                angles.append(angle)
            sum = 0
            for angle in angles:
                sum+=abs(angle)
            
            if 350 <= sum <= 370:
                area = cv2.contourArea(contour)
                if 2600 < area < 3300:
                    rectangles.append(approx)


    if len(rectangles) >= 2:
        
        # cv2.drawContours(image, rectangles, -1, (0, 255, 0), 2)

        # cv2.imwrite('Rectangles Detected.png', image)

        indexes_of_auto_recangles = []

        for rectangle in rectangles:
            x, y, w, h = cv2.boundingRect(rectangle)
            indexes_of_auto_recangles.append(int(x/width * 6) + 1)


        x1, _, _, _ = cv2.boundingRect(rectangles[0])
        x2, _, _, _ = cv2.boundingRect(rectangles[1])
        length_between_xs = abs(x1 - x2) / abs(indexes_of_auto_recangles[0] - indexes_of_auto_recangles[1])
        not_read_indexes = []

        for i in range(1, 7):
            if not i in indexes_of_auto_recangles:
                not_read_indexes.append(i)

        for index in not_read_indexes:
            min_index = -1
            min_value = 10
            for auto_index in indexes_of_auto_recangles:
                if abs(auto_index - index) < min_value:
                    min_index = auto_index
                    min_value = abs(auto_index - index)
            
            arr = rectangles[indexes_of_auto_recangles.index(min_index)]
            value_to_add_x = (index - min_index) * length_between_xs
            value_to_add_y = (min_index - index)

            rectangle_vertices = np.array([
                [arr[0][0][0] + value_to_add_x , arr[0][0][1] + value_to_add_y + 1], 
                [arr[1][0][0] + value_to_add_x , arr[1][0][1] + value_to_add_y - 1], 
                [arr[2][0][0] + value_to_add_x , arr[2][0][1] + value_to_add_y - 1], 
                [arr[3][0][0] + value_to_add_x , arr[3][0][1] + value_to_add_y + 1]
                ], np.int32)

            rectangle_contour = rectangle_vertices.reshape((-1, 1, 2))

            # cv2.drawContours(image, [rectangle_contour], 0, (0, 255, 0), 2)

            rectangles.append(rectangle_contour)
            indexes_of_auto_recangles.append(index)

        # print(rectangles)
        for index, rectangle in enumerate(rectangles):
            x, y, w, h = cv2.boundingRect(rectangle)
            cropped = original_image[y + default_length_between_rects_and_nums - 20:y+h + default_length_between_rects_and_nums + 20, x - 20:x+w+20]
            cropped_filename = f"../tmp/{indexes_of_auto_recangles[index]}.jpg"
            cv2.imwrite(cropped_filename, cropped)

        prev_rect_values = [0,0,0,0,0,0]
        prev_race = race

        for i in range(0, 6):
            # print(indexes_of_auto_recangles[i] - 1)
            prev_rect_values[indexes_of_auto_recangles[i] - 1] = rectangles[i]

    elif not prev_rect_values == False and abs(int(race) - int(prev_race)) < 10:
        print("prevvalues used")
        # print(prev_rect_values)
        for index, rectangle in enumerate(prev_rect_values):
            x, y, w, h = cv2.boundingRect(rectangle)
            cropped = original_image[y + default_length_between_rects_and_nums - 20:y+h + default_length_between_rects_and_nums + 20, x - 20:x+w+20]
            cropped_filename = f"../tmp/{index + 1}.jpg"
            cv2.imwrite(cropped_filename, cropped)
    elif len(rectangles) >= 1:
        print("1 rect used")

        # cv2.imwrite('Rectangles Detected.png', image)
        
        # cv2.drawContours(image, rectangles, -1, (0, 255, 0), 2)


        indexes_of_auto_recangles = []

        for rectangle in rectangles:
            x, y, w, h = cv2.boundingRect(rectangle)
            indexes_of_auto_recangles.append(int(x/width * 6) + 1)

        length_between_xs = default_length_between_rects
        not_read_indexes = []

        for i in range(1, 7):
            if not i in indexes_of_auto_recangles:
                not_read_indexes.append(i)

        for index in not_read_indexes:
            min_index = -1
            min_value = 10
            for auto_index in indexes_of_auto_recangles:
                if abs(auto_index - index) < min_value:
                    min_index = auto_index
                    min_value = abs(auto_index - index)
            
            arr = rectangles[indexes_of_auto_recangles.index(min_index)]
            value_to_add_x = (index - min_index) * length_between_xs
            value_to_add_y = (min_index - index)

            rectangle_vertices = np.array([
                [arr[0][0][0] + value_to_add_x , arr[0][0][1] + value_to_add_y + 1], 
                [arr[1][0][0] + value_to_add_x , arr[1][0][1] + value_to_add_y - 1], 
                [arr[2][0][0] + value_to_add_x , arr[2][0][1] + value_to_add_y - 1], 
                [arr[3][0][0] + value_to_add_x , arr[3][0][1] + value_to_add_y + 1]
                ], np.int32)

            rectangle_contour = rectangle_vertices.reshape((-1, 1, 2))

            # cv2.drawContours(image, [rectangle_contour], 0, (0, 255, 0), 2)

            rectangles.append(rectangle_contour)
            indexes_of_auto_recangles.append(index)

        # print(rectangles, indexes_of_auto_recangles)
        for index, rectangle in enumerate(rectangles):
            x, y, w, h = cv2.boundingRect(rectangle)
            cropped = original_image[y + default_length_between_rects_and_nums - 20:y+h + default_length_between_rects_and_nums + 20, x - 20:x+w+20]
            cropped_filename = f"../tmp/{indexes_of_auto_recangles[index]}.jpg"
            cv2.imwrite(cropped_filename, cropped)

        prev_rect_values = [0,0,0,0,0,0]

        for i in range(0, 6):
            # print(indexes_of_auto_recangles[i] - 1)
            prev_rect_values[indexes_of_auto_recangles[i] - 1] = rectangles[i]