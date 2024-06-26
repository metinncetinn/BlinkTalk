import cv2 as cv
import numpy as np

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (255,0,0)
RED = (0,0,255)
CYAN = (255,255,0)
YELLOW =(0,255,255)
MAGENTA = (255,0,255)
GRAY = (128,128,128)
GREEN = (0,255,0)
PURPLE = (128,0,128)
ORANGE = (0,165,255)
PINK = (147,20,255)
points_list =[(200, 300), (150, 150), (400, 200)]

def drawColor(img, colors):
    x, y = 0,10
    w, h = 20, 30
    for color in colors:
        x += w+5 
        cv.rectangle(img, (x-6, y-5 ), (x+w+5, y+h+5), (10, 50, 10), -1)
        cv.rectangle(img, (x, y ), (x+w, y+h), color, -1)

def colorBackgroundText(img, text, font, fontScale, textPos, textThickness=1, textColor=(0,255,0), bgColor=(0,0,0), pad_x=3, pad_y=3):
    (t_w, t_h), _= cv.getTextSize(text, font, fontScale, textThickness)
    x, y = textPos
    cv.rectangle(img, (x-pad_x, y+ pad_y), (x+t_w+pad_x, y-t_h-pad_y), bgColor, -1)
    cv.putText(img, text, textPos, font, fontScale, textColor, textThickness)
    return img

def textWithBackground(img, text, font, fontScale, textPos, textThickness=1, textColor=(0,255,0), bgColor=(0,0,0), pad_x=3, pad_y=3, bgOpacity=0.5):
    (t_w, t_h), _= cv.getTextSize(text, font, fontScale, textThickness)
    x, y = textPos
    overlay = img.copy()
    cv.rectangle(overlay, (x-pad_x, y+ pad_y), (x+t_w+pad_x, y-t_h-pad_y), bgColor, -1)
    new_img = cv.addWeighted(overlay, bgOpacity, img, 1 - bgOpacity, 0)
    cv.putText(new_img, text, textPos, font, fontScale, textColor, textThickness)
    return new_img

def textBlurBackground(img, text, font, fontScale, textPos, textThickness=1, textColor=(0,255,0), kernel=(33,33), pad_x=3, pad_y=3):
    (t_w, t_h), _= cv.getTextSize(text, font, fontScale, textThickness)
    x, y = textPos
    blur_roi = img[y-pad_y-t_h: y+pad_y, x-pad_x:x+t_w+pad_x]
    img[y-pad_y-t_h: y+pad_y, x-pad_x:x+t_w+pad_x] = cv.blur(blur_roi, kernel)
    cv.putText(img, text, textPos, font, fontScale, textColor, textThickness)
    return img

def fillPolyTrans(img, points, color, opacity):
    list_to_np_array = np.array(points, dtype=np.int32)
    overlay = img.copy()
    cv.fillPoly(overlay, [list_to_np_array], color)
    new_img = cv.addWeighted(overlay, opacity, img, 1 - opacity, 0)
    cv.polylines(img, [list_to_np_array], True, color, 1, cv.LINE_AA)
    return new_img

def rectTrans(img, pt1, pt2, color, thickness, opacity):
    overlay = img.copy()
    cv.rectangle(overlay, pt1, pt2, color, thickness)
    new_img = cv.addWeighted(overlay, opacity, img, 1 - opacity, 0)
    return new_img
