import numpy as np
import matplotlib
import cv2
import math


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow('Sliders')
cv2.resizeWindow('Sliders', 700, 500)
cv2.createTrackbar('ker_type', 'Sliders', 0, 2, nothing)
cv2.createTrackbar('ker_size', 'Sliders', 0, 20, nothing)
cv2.createTrackbar('morph_operation', 'Sliders', 0, 4, nothing)
cv2.createTrackbar('iteration_no', 'Sliders', 0, 10, nothing)
cv2.createTrackbar('l1', 'Sliders', 0, 255, nothing)
cv2.createTrackbar('l2', 'Sliders', 0, 255, nothing)
cv2.createTrackbar('l3', 'Sliders', 0, 255, nothing)
cv2.createTrackbar('h1', 'Sliders', 0, 255, nothing)
cv2.createTrackbar('h2', 'Sliders', 0, 255, nothing)
cv2.createTrackbar('h3', 'Sliders', 0, 255, nothing)
cv2.createTrackbar('contours', 'Sliders', 0, 1, nothing)
cv2.createTrackbar('side1', 'Sliders', 0, 100, nothing)
cv2.createTrackbar('side2', 'Sliders', 0, 100, nothing)


while cap.isOpened() and cv2.waitKey(1) != 27:
    ker_t = cv2.getTrackbarPos('ker_type', 'Sliders')
    size = cv2.getTrackbarPos('ker_size', 'Sliders')
    op = cv2.getTrackbarPos('morph_operation', 'Sliders')
    itr = cv2.getTrackbarPos('iteration_no', 'Sliders')

    ker = None
    if ker_t == 1 and size > 0:
        ker = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    elif ker_t == 2 and size > 0:
        ker = cv2.getStructuringElement(cv2.MORPH_CROSS, (size, size))
    l1 = cv2.getTrackbarPos('l1', 'Sliders')
    l2 = cv2.getTrackbarPos('l2', 'Sliders')
    l3 = cv2.getTrackbarPos('l3', 'Sliders')
    h1 = cv2.getTrackbarPos('h1', 'Sliders')
    h2 = cv2.getTrackbarPos('h2', 'Sliders')
    h3 = cv2.getTrackbarPos('h3', 'Sliders')

    ret, frame = cap.read()
    if ret == 0:
        print "CAPTURE ERROR"
        # break
    cv2.imshow('Raw', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(hsv, np.array([l1, l2, l3]),
                           np.array([h1, h2, h3]))

    if itr <= 0:
        itr = 1

    if op == 1:
        filtered = cv2.erode(filtered, ker, iterations=itr)
    elif op == 2:
        filtered = cv2.dilate(filtered, ker, iterations=itr)
    elif op == 3:
        filtered = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, ker)
    elif op == 4:
        filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, ker)

    draw = cv2.getTrackbarPos('contours', 'Sliders')

    if draw == 1:
        _, contours, _ = cv2.findContours(filtered, cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)

        side1 = cv2.getTrackbarPos('side1', 'Sliders')
        side2 = cv2.getTrackbarPos('side2', 'Sliders')

        opt_ratio = float(max(side1, side2))/min(side1, side2)

        best_box = None
        best_dif = opt_ratio*0.5

        for contour in contours:
            rect = cv2.minAreaRect(contour)
            points = cv2.boxPoints(rect)
            pt0 = points[0]
            dist = []
            for pt in points[1:]:
                dist.append(math.sqrt((pt0[0]-pt[0])**2 + (pt0[1]-pt[1])**2))
            dist.sort()
            if dist[0] <= 0:
                continue
            ratio = float(dist[1])/dist[0]
            if abs(ratio-opt_ratio) < best_dif:
                best_box = points
                best_dif = abs(ratio-opt_ratio)

        if best_box is not None:
            box = np.intp(best_box)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 3)

    cv2.imshow('Filtered', filtered)
    cv2.imshow('Final', frame)
