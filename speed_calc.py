import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import math


cap = cv2.VideoCapture(0)
startx = -1

def captu(): 
    print("captu called")
    global startx
    startx = -1    
    ####### capture startx
    _, prevc = cap.read()
    prevc= cv2.flip(prevc, 1)

    while True:
        _, newc = cap.read()
        newc = cv2.flip(newc, 1)
        diffc = cv2.absdiff(prevc, newc)
        diffc = cv2.cvtColor(diffc, cv2.COLOR_BGR2GRAY)
        diffc = cv2.blur(diffc, (4,4))
        _, diffc = cv2.threshold(diffc, 10,255, cv2.THRESH_BINARY)
        _,contorc,_ = cv2.findContours(diffc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contc in contorc :
            if cv2.contourArea(contc) > 30000:
                (x1c,y1c),rad = cv2.minEnclosingCircle(contc)
                if x1c < 545 and x1c > 105:
                    startx = x1c
                
        prevc = newc.copy()

        cv2.imshow("diffc", diffc)


        if cv2.waitKey(1) == 27 or startx != -1:

            break

    return startx

################################################
def right():
    print("from right")
    endxr = -1
    global startx
    start_time = time.time()
    _, prevr = cap.read()
    prevr= cv2.flip(prevr, 1)
    while True:
        _, newr = cap.read()
        newr = cv2.flip(newr, 1)
        diffr = cv2.absdiff(prevr, newr)
        diffr = cv2.cvtColor(diffr, cv2.COLOR_BGR2GRAY)
        diffr = cv2.blur(diffr, (4,4))
        _, diffr = cv2.threshold(diffr, 10,255, cv2.THRESH_BINARY)
        _,contorr,_ = cv2.findContours(diffr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contr in contorr :
            if cv2.contourArea(contr) > 30000:
                (x,y,w,h) = cv2.boundingRect(contr) 
                (x1r,y1r),rad = cv2.minEnclosingCircle(contr)
                cv2.rectangle(prevr, (x,y), (x+w,y+h), (0,255,0), 2)
                if x1r > 550:                    
                    endxr = x1r
                    end_time = time.time()
                    print("it took {}".format(end_time-start_time))
                    cv2.putText(prevr, "speed:{} px/sec".format(math.trunc(np.sqrt((550-startx)**2)/(end_time-start_time))),(50,100),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                    break
                    
        cv2.imshow("right", prevr)
        prevr = newr.copy()

        if endxr > 550 or cv2.waitKey(1) == 27:

            break
    return None

def left():
    global startx
    endx = 700
    print("from left")
    start_time = time.time()
    _, prev = cap.read()
    prev= cv2.flip(prev, 1)
    while True:     
        _, new = cap.read()
        new = cv2.flip(new, 1)
        diff = cv2.absdiff(prev, new)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        diff = cv2.blur(diff, (4,4))
        _, diff = cv2.threshold(diff, 10,255, cv2.THRESH_BINARY)
        _,contor,_ = cv2.findContours(diff, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cont in contor :
            if cv2.contourArea(cont) > 30000:
                
                (x,y,w,h) = cv2.boundingRect(cont) 
                (x1,y1),rad = cv2.minEnclosingCircle(cont)
                cv2.rectangle(prev, (x,y), (x+w,y+h), (0,255,0), 2)
                if x1 < 100:                      
                    endx = x1
                    end_time = time.time()
                    print("it took {}".format(end_time-start_time))
                    cv2.putText(prev, "speed:{} px/sec".format(math.trunc(np.sqrt((startx - x1)**2 )/(end_time-start_time))),(50,100),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

                    break
                    
        cv2.imshow("left", prev)
        prev = new.copy()

        if endx < 100 or cv2.waitKey(1) == 27:
            break
    return None

############ CAPTURE ENDX    ###########################

while True : 
    if captu() < 150:
        right()    
    else:
        left()

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()


