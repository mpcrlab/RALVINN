__author__ = 'circleupx'
# Keep Track of any blue objects using OpenCV
# Import OpenCV
import cv2
# Import Numpy
import numpy as np

# Open WebCam
camera_feed = cv2.VideoCapture(0)

# infinite loop
while (1):

    # Read WebCam
    _, frame = camera_feed.read()
    # Convert the current frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Define the threshold for finding a blue object with hsv.
    # The numbers in the array represent HSV colors, not RGB. If you want to track a different color then you must
    # convert from RGB to HSV. Python has a module for that https://docs.python.org/2/library/colorsys.html

    # Lower Limits of Blue
    lower_blue = np.array([100, 100, 100])
    # Higher Limit of Blue
    upper_blue = np.array([130, 255, 255])

    # Create a mask where anything blue appears white and everything else is black
    # inRage Checks if array elements lie between the elements of two other arrays.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Get rid of background noise
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.erode(mask, element, iterations=2)
    mask = cv2.dilate(mask, element, iterations=2)
    mask = cv2.erode(mask, element)

    # Create Contours for all blue objects
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea

    object_line = cv2.line(mask, )


    # Creates a box to keep track of blue objects
    if bestContour is not None:
        x, y, w, h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)



        # Show the original camera feed with a the tracking box
    cv2.imshow('frame', frame)
    # Show the contours in a seperate window
    cv2.imshow('mask', mask)
    # Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF
    # If escape is pressed close all windows
    if k == 27:
        break

# End
cv2.destroyAllWindows()
