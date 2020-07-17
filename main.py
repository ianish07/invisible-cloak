
import numpy as np
import time
import cv2

cap = cv2.VideoCapture(0)    # '0' refers to the primary camera, will change (eg. '1'/'2'') for any external ones
## Allow the system to sleep for 2 seconds before the webcam starts
time.sleep(2)

background = 0

for i in range(30):
    #capturing the background for initial few secs(here in range 30)
    ret,background = cap.read()

while (cap.isOpened()):
    # capturing every frame till the webcam is open
    ret, img = cap.read()
    if not ret:
        break
    ## Convert the color space from BGR to HSV
    hsv  = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    ## Generat masks to detect red color (color may vary depending upon your choice)
    ##values [0,120,70] represents Hue(Color Portion/which color you want to identify), Saturation(amt of grey), Value(Brightness)
    lower_red = np.array([0,120,70])
    higher_red = np.array([10,255,255])

    #separating our cloak part,i.e. looking for cloak in hsv in range of lower & higher red
    mask1 = cv2.inRange(hsv,lower_red,higher_red)

    lower_red = np.array([170, 120, 60])
    higher_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, higher_red)

    mask1 = mask1 + mask2  #segmenting any shade of red (from 0-10 or 170-180) and storing it in mask1

    ## morph_open basically removes any noise from the image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8) ,iterations = 2)  #iterations for better result
    ## morph_dialate smooths out the image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations = 1)

    ## Create an inverted mask to segment out the red color from the frame(i.e, the cloak)
    mask2 = cv2.bitwise_not((mask1))

    ## Segment the red color part out of the frame
    res1 = cv2.bitwise_and(img,img, mask=mask2)

    ## Create image showing static background frame pixels only for the masked region i.e, Subsituting the cloak part
    res2 = cv2.bitwise_and(background,background, mask=mask1)

    ## Linearly adding both image for final output
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("magic", final_output)
    k = cv2.waitKey(10)
    ## Closing the window esc is entered
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()