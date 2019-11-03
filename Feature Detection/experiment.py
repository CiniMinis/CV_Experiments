import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

EXIT_KEY = 'q'
CAP_KEY = 'p'
SCALE = 5
MAX_MATCHES = 200
MIN_MATCHES = 10
RANSAC_REPROJ = 10
RANSAC_ACCURACY = 0.5

points = []


def ShapeGenerator(event, x, y, flag, param):
    if is_first_pic and event == cv2.EVENT_LBUTTONDOWN:
        point.append([x,y])

cap = cv2.VideoCapture(0)
cv2.namedWindow('feed')
print("Press P to take picture 1")
while cap.isOpened() and cv2.waitKey(1) != ord(CAP_KEY):
    _, feed = cap.read()
    cv2.imshow('feed', feed)
is_first_pic = True

is_first_pic = False
img1 = feed
print("Press P to take picture 2")
while cap.isOpened() and cv2.waitKey(1) != ord(CAP_KEY):
    _, feed = cap.read()
    cv2.imshow('feed', feed)
img2 = feed
print("Calculating")
# Initiate ORB detector
orb = cv2.ORB_create()
# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# Match descriptors.
unfiltered_matches = bf.match(des1,des2)
matches=[]
for i in range(len(unfiltered_matches)-1):
    if unfiltered_matches[i].distance < 0.8*unfiltered_matches[i+1].distance:
        matches.append(unfiltered_matches[i])
# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)
# Draw first 10 matches.
matches_to_use = min(MAX_MATCHES, len(matches)-1)
matches = matches[:matches_to_use]

if matches_to_use <= MIN_MATCHES:
    print("Insufficient point number")
    exit()

# apply ransac
src_pts = np.float32([kp1[match.queryIdx].pt for match in matches])
dst_pts = np.float32([kp2[match.trainIdx].pt for match in matches])
F, mask = cv2.findFundamentalMat(src_pts.reshape(-1,1,2), dst_pts.reshape(-1,1,2), cv2.RANSAC, RANSAC_REPROJ, RANSAC_ACCURACY)
match_mask = mask.ravel().tolist()

# draw matches
params = dict(matchesMask = match_mask)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, **params)
# filter points
good_src = [src_pts[i] for i in range(len(src_pts)) if match_mask[i] == 1]
good_dst = [dst_pts[i] for i in range(len(dst_pts)) if match_mask[i] == 1]
print("Found {} good matches".format(len(good_src)))

# print arrows
arrows = img1.copy()
for i in range(len(good_src)):
    # print(good_src[i])
    cv2.arrowedLine(arrows, tuple(good_src[i]), tuple(good_dst[i]), (0, 100, 255))
cv2.imshow('matches', arrows)
cv2.imshow('origin', img1)
cv2.waitKey()
cv2.destroyAllWindows()
cap.release()