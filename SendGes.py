import cv2
import numpy as np
import math
import os


p = 0
q = 0

# Test_Server_py_START

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

BC_PORT = 9012
# port for ip broadcast
import sys
import time
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# Include IP headers: setsockopt
s.sendto(ip, ('<broadcast>', BC_PORT))
# Send data to the socket


# Test_Server_py_END


cap = cv2.VideoCapture(0)
cam = 1
while True:

    while(cam):
        ret, img = cap.read()
        # Deleting this is causing an error,dont know why!
        cv2.rectangle(img, (250, 250), (50, 50), (0, 255, 0), 1)
        crop_img = img[50:250, 50:250]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cv2.imshow('Thresholded', thresh1)
        _, contours, hierarchy = cv2.findContours(
            thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        max_area = -1
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if(area > max_area):
                max_area = area
                ci = i
        cnt = contours[ci]
        x, y, w, h = cv2.boundingRect(cnt)
        # Red box in the img window from the countours
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape, np.uint8)
        # contour window green
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        # contour window red line
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0

        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img, start, end, [0, 255, 0], 2)
            # cv2.circle(crop_img,far,5,[0,0,255],-1)

        if count_defects == 1:
            cv2.putText(img, "defect 1", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            if p == 1:
                q = 1
                cam = 0
        elif count_defects == 2:
            cv2.putText(img, "defect 2", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        elif count_defects == 3:
            cv2.putText(img, "defect 3", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(img, "defect 4", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 5:
            cv2.putText(img, "defect 5", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            p = 1

        else:
            cv2.putText(img, "Default defect", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        # cv2.imshow('end', crop_img)  #Crop_img part of screen(The green box)
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            exit()

    if p == 1 and q == 1:

        import SimpleHTTPServer
        import SocketServer
        import sys
        import time
        import socket

        cap.release()
        cv2.destroyAllWindows()
        p = 0
        q = 0
        # START HTTP server
        PORT = 8000
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        Handler.extensions_map.update({
            '.webapp': 'application/x-web-app-manifest+json',
        })

        httpd = SocketServer.TCPServer(("", PORT), Handler)

        httpd.serve_forever()

        # END ~ Server Created

    #cam = 1
    #cap = cv2.VideoCapture(0)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        exit()

cap.release()
cv2.destroyAllWindows()
