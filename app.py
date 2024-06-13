import numpy as np
import cv2 

def isTouching(box1, box2): #check if two boxes are making contact 
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
        return True
    else:
        return False

TrDict = {'csrt': cv2.legacy.TrackerCSRT_create,
          'kcf': cv2.legacy.TrackerKCF_create,
          'boosting': cv2.legacy.TrackerBoosting_create,
          'mil': cv2.legacy.TrackerMIL_create,
          'tld': cv2.legacy.TrackerTLD_create,
          'medianflow': cv2.legacy.TrackerMedianFlow_create,
          'mosse':cv2.legacy.TrackerMOSSE_create}
punches_landed = 0

#mosse is good for tracking the heads
#

bodies = cv2.legacy.MultiTracker_create() # create list of trackers using MultiTracker object
hands = cv2.legacy.MultiTracker_create()

vid = cv2.VideoCapture('assets/match.mp4')

ret, frame = vid.read()
k=2 # number of objects we're tracking
for i in range(k): #make a range of interest for each object we want and add a tracker to them
    cv2.imshow('Frame',frame)
    bbi = cv2.selectROI('Frame', frame) # region of interest
    bodies_i = TrDict['csrt']() # tracker
    bodies.add(bodies_i,frame,bbi) # add i'th tracker 


while True:
    ret, frame = vid.read()
    if not ret:
        break
    (success, boxes) = bodies.update(frame)
    for box in boxes:
        (x,y,w,h)= [int(a) for a in box]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
    for i in range(len(boxes)-1):
        if isTouching(boxes[i],boxes[i+1]):
            cv2.putText(frame, "punch landed", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3) # if movements are detected, display text stating boxers are active
            print('the boxers are in range')
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) == ord('q'): #press q to break 
        break

vid.release() # stops video


#cv2.imshow('Image', img)
cv2.waitKey(0) 
cv2.destroyAllWindows() # destroy all windows


'''diff = cv2.absdiff(frame1, frame2) #get difference between 1st and 2nd frame
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # difference converted into grayscale
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    dil = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # find contours

    
    for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour) #give us x, y coord with width and height
            


            #if cv2.contourArea(contour) <700: # if area is less than 700, do nothing
                 #continue
            #cv2.rectangle(frame1, (x,y), (x+w,y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "boxers active", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3) # if movements are detected, display text stating boxers are active
    cv2.drawContours(frame1, contours, -1, (0,255,0), 2) # draw contours on orig frame

    print('Contour 1:' +str(contours[0]))
    print('Contour 2:' +str(contours[1]))
    print(len(contours))
    #if are_contours_touching(contour[1],contour[3]):
    #     print('hi')

    cv2.imshow('feed', frame1) #takes the frame1, and shows it (this frame has the contours)
    frame1 = frame2
    ret, frame2 = vid.read()
'''