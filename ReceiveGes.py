import cv2
import numpy as np
import math
import urllib
import select, socket 
import os

k = 0
m = 0
cam = 1

####Code for receiving sender's IP

import select, socket 

port = 9012  # where do you expect to get a msg?
bufferSize = 1024 # whatever you need

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#address family and connection type 
s.bind(("", port))
s.setblocking(0)

ip_count = 0
#takes ip
while True:
    result = select.select([s],[],[])
    ip = result[0][0].recv(bufferSize)
    #print ip
    break
    

print("ip successfully received")
print("The ip address of sender is:"+ip)
print("Ready to receive the data.")
print("-------------------------------------------")


####IP is received!

cap = cv2.VideoCapture(0)

while True:
    
    while(cam):
        ret, img = cap.read()
        cv2.rectangle(img,(250,250),(50,50),(0,255,0),0) ###green rectangle
        crop_img = img[50:250, 50:250]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)##optimal threahold value
        cv2.imshow('Thresholded', thresh1)
        _, contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)##retrieves all of the contours

        max_area = -1
        for i in range(len(contours)):##finds outer boundary contour
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
        cnt=contours[ci]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0) #red box from the countours
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape,np.uint8)#uint8 data type
        cv2.drawContours(drawing,[cnt],0,(0,255,0),0)  #contour window green
        cv2.drawContours(drawing,[hull],0,(0,0,255),0) #contour window red line
        hull = cv2.convexHull(cnt,returnPoints = False)#returns indices of contour point corresponding to the hull point
        defects = cv2.convexityDefects(cnt,hull)
        count_defects = 0
        
        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img,far,1,[0,0,255],-1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img,start,end,[0,255,0],2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)    
        
        if count_defects == 1:
            cv2.putText(img,"defect 1", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            k =1
        elif count_defects == 2:
            cv2.putText(img, "defect 2", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 3:
            cv2.putText(img,"defect 3", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(img,"defect 4", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 5:
            cv2.putText(img,"defect 5", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            if k ==1:
                m = 1
                cam = 0
        
        else:
            cv2.putText(img,"Default defect", (50,50),\
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_img)  #Crop_img part of screen(The green box)
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))#horizontal stack
        cv2.imshow('Contours', all_img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            exit()

    if k ==1 and m ==1: #k and m are set to 1 which shows fingers went 1 to 5
    

        k = 0
        cam = 0
        cap.release()
        cv2.destroyAllWindows()
        testfile = urllib.URLopener()
        

        from urllib2 import urlopen
        import re

        urlpath =urlopen("http://"+ip+":8000/SEND/")
        string = urlpath.read().decode('utf-8')

         #the pattern actually creates duplicates in the list
        pattern = re.compile('[\w\s,!@#$%^&*()=-]*[.][\w]{1,4}"')
        filelist = pattern.findall(string)

        print("Received files are:\n")
        
        for filenames in filelist:
            print(filenames[:-1])
            receive_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "RECEIVE")
            fullfilename = os.path.join(receive_location, filenames[:-1])
            testfile.retrieve("http://"+ip+":8000/SEND/"+filenames[:-1], fullfilename)

        print("Goto Received folder to see the files.")   
    #cam = 1
    #cap = cv2.VideoCapture(0)

    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
     
cap.release()
cv2.destroyAllWindows()
