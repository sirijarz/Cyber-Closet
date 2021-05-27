import cv2
import imutils
import numpy as np
import CollectionOfTops as cc
import random

def fashion():
    video = cv2.VideoCapture(0)
    images = cc.loadImages()
    thres = [130, 40, 75, 130]
    size = 180
    currentClothId = 1
    th = thres[0]
    while True:
        (ret, frame_to_try) = video.read()
        frame_to_try = cv2.flip(frame_to_try, 1, 0)
        top = images[currentClothId]
        resized = imutils.resize(frame_to_try, width=800)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # only works if circle of radius 30 exists
                if r > 30:
                    # draw circle and center of circle contour
                    cv2.circle(frame_to_try, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(frame_to_try, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    # adjust size of tshirt according to radius of circle
                    size = r * 3
        if size > 350:
            size = 350
        elif size < 100:
            size = 100

        top = imutils.resize(top, width=size)

        f_height = frame_to_try.shape[0]
        f_width = frame_to_try.shape[1]
        t_height = top.shape[0]
        t_width = top.shape[1]
        height = int(f_height / 2 - t_height / 2)
        width = int(f_width / 2 - t_width / 2)
        rows, cols, channels = top.shape
        topGray = cv2.cvtColor(top, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(topGray, th, 255, cv2.THRESH_BINARY_INV)
        inverted_mask = cv2.bitwise_not(mask)
        roi = frame_to_try[height:height + t_height, width:width + t_width]
        image_background = cv2.bitwise_and(roi, roi, mask=inverted_mask)
        image_foreground = cv2.bitwise_and(top, top, mask=mask)

        top = cv2.add(image_background, image_foreground)
        # cv2.imshow("tshirt", mask)

        frame_to_try[height:height + t_height, width:width + t_width] = top
        font = cv2.FONT_HERSHEY_SIMPLEX  # Creates a font
        x = 10  # position of text
        y = 20  # position of text

        cv2.putText(frame_to_try, "press n to try the next top & p for previous", (x, y), font, .5, (255, 255, 255),
                    1)  # Draw the text
        cv2.namedWindow("Let us try on some tops!", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Let us try on some tops!", int(frame_to_try.shape[1] * 1.4), int(frame_to_try.shape[0] * 1.4))
        cv2.imshow('Let us try on some tops!', frame_to_try)
        key = cv2.waitKey(10)
        if key & 0xFF == ord('n'):
            if currentClothId == len(images) - 1:
                print("Out of Stock!")
            else:
                currentClothId += 1
                th = thres[currentClothId]
        if key & 0xFF == ord('c'):  # save on pressing 'y'
            rand = random.randint(1, 999999)

            cv2.imwrite('output/'+str(rand)+'.png', frame_to_try)

        if key & 0xFF == ord('p'):
            if currentClothId == -1:
                print("Out of Stock!")
            else:
                currentClothId -= 1

        if key == 27:
            break
    return

fashion()
