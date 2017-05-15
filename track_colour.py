import cv2
import numpy as np

from controlled_variable import ControlledVariable

def compute_contours(cns):
    """Centroid stuff"""
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    return center, radius, (x, y)


# illumination can be a problem due to colour value
# hsv? yuv?- define range (try hsv later)

device = cv2.VideoCapture(0)

# Colour range - hsv. H110-130 blueish.
# sv - right the way up to allow for illumination

# Lego thing: [90   0 240] [120 255 255]
# Green skittle - [ 35 130  80] [ 95 255 255]

lh = ControlledVariable(0, 255, 90,  (ord('a'), ord('s')))
uh = ControlledVariable(0, 255, 120, (ord('k'), ord('l')))
lv = ControlledVariable(0, 255, 240, (ord('z'), ord('x')))
hv = ControlledVariable(0, 255, 255, (ord('m'), ord('n')))
ls = ControlledVariable(0, 255, 10,  (ord('q'), ord('w')))
hs = ControlledVariable(0, 255, 255, (ord('o'), ord('p')))
while True:
    ret, frame = device.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_range = np.array([lh.value, ls.value, lv.value], np.uint8)
    upper_range = np.array([uh.value, hs.value, hv.value], np.uint8)

    # Create a mask around that colour
    inrange = cv2.inRange(hsv, lower_range, upper_range)


    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(inrange, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find contours in the mask and initialize the current
    # (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    
    if len(cnts) >0:
        center, radius, (x, y) = compute_contours(cnts)
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
            cv2.putText(frame,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            cv2.putText(frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            _, w, _ = frame.shape
            hw = w / 2
            if x > hw + 10:
                print("Driving right")
            elif x < hw - 10:
                print("Driving left")
            else:
                print("Ramming speed!!!")
            
            
    cv2.imshow("Ranged", inrange)
    cv2.imshow("Frame", frame)
    print lower_range, upper_range
    k = cv2.waitKey(1)
    if k == 27:
        break
    lh.handle_key(k)
    uh.handle_key(k)
    ls.handle_key(k)
    hs.handle_key(k)
    lv.handle_key(k)
    hv.handle_key(k)
    

device.release()
cv2.destroyAllWindows()
