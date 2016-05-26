import cv2
import numpy as np

filepath = "cat1.jpg"
img_bgr = cv2.imread(filepath,1)
img = cv2.imread(filepath,0)

height, width = img.shape[:2]
if height > 900:
    height = height/10
    width = width/10
    factor = 300
elif height < 200:
    height = height*2
    width = width*2
    factor = 300
else:
    factor = 500

img = cv2.resize(img,(width,height),interpolation = cv2.INTER_CUBIC)
img = cv2.medianBlur(img,5)
img_bgr = cv2.resize(img_bgr,(width,height),interpolation = cv2.INTER_CUBIC)


circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,factor,param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img_bgr,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img_bgr,(i[0],i[1]),2,(0,0,255),3)


xc,yc,r = circles[0][0]

H, W = img.shape
x, y = np.meshgrid(np.arange(W), np.arange(H))
d2 = (x - xc)**2 + (y - yc)**2
mask = d2 > r**2

inside = np.ma.masked_where(mask, img)
average_color = inside.mean()
print average_color

font = cv2.FONT_HERSHEY_SIMPLEX

if average_color > 60:
    print "Cataract"
    cv2.putText(img_bgr,'Cataract',(1,60), font, 2,(255,255,255),2,cv2.LINE_AA)
else:
    cv2.putText(img_bgr,'Not Cataract',(1,60), font, 2,(255,255,255),2,cv2.LINE_AA)
    print "Not Cataract"


cv2.imshow('Detected Circle',img_bgr)
cv2.waitKey(0)
