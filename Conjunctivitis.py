import cv2
import numpy as np

filepath = "rinnegan.jpg"
img_bgr = cv2.imread(filepath,1)
img = cv2.imread(filepath,0)

height, width = img.shape[:2]
if height > 900 or width>900:
    height = height/10
    width = width/10
    factor = 300
elif height < 200:
    height = height*2
    width = width*2
    factor = 300
else:
    factor = 500

factor = 500
#img = cv2.resize(img,(width,height),interpolation = cv2.INTER_CUBIC)
img = cv2.medianBlur(img,5)
#img = cv2.GaussianBlur(img,(5,5),0)

img_bgr = cv2.resize(img_bgr,(width,height),interpolation = cv2.INTER_CUBIC)
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,factor,param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img_bgr,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img_bgr,(i[0],i[1]),2,(0,0,255),3)
    break

xc,yc,r = circles[0][0]

#ellipse
a = 3*r
b=6*r

#pupil
a1 = r*3

H, W = img.shape
x, y = np.meshgrid(np.arange(W), np.arange(H))
d2 = (x - xc)**2 + (y - yc)**2
mask = d2 > r**2

inside = np.ma.masked_where(mask, img)
average_color = inside.mean()
print average_color
print r,xc,yc

centre = (xc,yc)

#cv2.ellipse(img_bgr,(xc,yc), axes=(10,20), angle=0, startAngle=10, end_angle=360, color=(255,0,0))
el = cv2.ellipse(img_bgr,(xc,yc),(b,a),0,0,360,(0,255,0),1)
height, width = img.shape[:2]
blank_image = np.zeros((height,width,3), np.uint8)
cv2.ellipse(blank_image,(xc,yc),(b,a),0,0,360,(255,255,255),-1)
result = np.bitwise_and(img_bgr,blank_image)
cv2.circle(result,(i[0],i[1]),i[2]*3,(0,0,0),-1)
average_color1 = result.mean()
print average_color1
cv2.imshow('Result',result)
cv2.imwrite('Result.jpg',result)
b,g,r = cv2.split(result)
print r.mean()
if r.mean() >= 20:
    print "Conjunctivitis"
else:
    print "Not Conjunctivitis"
cv2.imshow('Blank Image2',r)
cv2.imwrite('Blank Image2.jpg',r)
#font = cv2.FONT_HERSHEY_SIMPLEX

#if average_color > 60:
    #print "Cataract"
    #cv2.putText(img_bgr,'Cataract',(1,60), font, 2,(255,255,255),2,cv2.LINE_AA)
#else:
    #cv2.putText(img_bgr,'Not Cataract',(1,60), font, 2,(255,255,255),2,cv2.LINE_AA)
    #print "Not Cataract"


H1,W1 = img.shape
x, y = np.meshgrid(np.arange(W1), np.arange(H1))
d2 = (x - xc)**2 + (y - yc)**2
mask1 = d2 > a1**2

#inside1 = np.ma.masked_where(el,mask1)
#average_color1 = inside1.mean()

#print average_color1
print el.shape
#print mask1
cv2.circle(img_bgr,(i[0],i[1]),i[2]*3,(0,255,0),1)
cv2.imshow('Detected Circle',img_bgr)
cv2.imshow('Blank Image',blank_image)
cv2.imwrite('Detected Circle.jpg',img_bgr)
cv2.imwrite('Blank Image.jpg',blank_image)
cv2.waitKey(0)
