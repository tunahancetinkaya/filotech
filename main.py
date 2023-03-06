import numpy as np
import cv2
import imutils

vid = cv2.VideoCapture(0)

while(True):

    ret, img = vid.read()
    #img = imutils.resize(img, width=1080)
    maskk = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    kirmizi_min=np.array([0,100,20])
    kirmizi_maks=np.array([10,255,255])
    #imgg = img.copy()
    maske = cv2.inRange(maskk, kirmizi_min, kirmizi_maks)
    img = cv2.bitwise_and(img, img, mask=maske)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 55, 100)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        rect = cv2.minAreaRect(contour)
        alan = cv2.contourArea(contour)
        if alan < 500000 and alan > 20000:
            #cv2.drawContours(imgg, contour, -1, (255, 0, 0), 3)
            moments = cv2.moments(contour)
            if moments['m00'] != 0.0:  # kütle merkezini bulma
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
            #cv2.circle(imgg, (cx, cy), 5, (255, 0, 0), -1)
            # print(cx,cy)
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)  # şekil tespiti için köşelere bakma
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
            if len(approx) > 5:
                sekil = "daire"
                #cv2.putText(imgg, 'hedef', (x, y),
                 #           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                if cx>=360 and cx <= 720 and cy >=208 and cy <=416:
                    print("--------------------------\n\n\n\n")
                    print("görev tamamlandı\n\n\n\n")
                    print("--------------------------\n\n\n\n")
                elif cx <360:
                    print("--------------------------\n\n\n\n")
                    print("sol\n\n\n\n")
                    print("--------------------------\n\n\n\n")
                elif cx>720:
                    print("--------------------------\n\n\n\n")
                    print("sağ\n\n\n\n")
                    print("--------------------------\n\n\n\n")
                else:
                    print("--------------------------\n\n\n\n")
                    print("düz\n\n\n\n")
                    print("--------------------------\n\n\n\n")
    # cv2.line(imgg, (360, 624), (360, 0), (0, 255, 0), 3)
    # cv2.line(imgg, (720, 624), (720, 0), (0, 255, 0), 3)
    # cv2.line(imgg, (360, 208), (720, 208), (0, 255, 0), 3)
    # cv2.line(imgg, (360, 416), (720, 416), (0, 255, 0), 3)
    cv2.imshow('output',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(1)
cv2.destroyAllWindows()
