from lib2to3.pygram import pattern_symbols
import dlib
import cv2
import numpy as np

detector = dlib.get_frontal_face_detector()
path = '/Users/GakutoSasabe/Desktop/Research/OpencvEyetracking/shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(path)

def is_close(y0,y1): #目が閉じているか判定する関数
    if abs(y0 - y1) < 10:
        return True
    return False

def get_center(gray_img):#二値化された目画像から瞳の重心を求める
    moments = cv2.moments(gray_img, False)
    try:
        
        return int(moments['m10']/moments['m00']), int(moments['m01'] / moments['m00'])
    except:
        return None

def p(img, parts, eye):
    if eye[0]:
        cv2.circle(img, eye[0], 3, (255,255,0), -1)
    if eye[1]:
        cv2.circle(img, eye[1], 3, (255,255,0), -1)  
    for i in parts:
        cv2.circle(img, (i.x, i.y), 3, (255, 0, 0), -1)

    cv2.imshow("me", img)  

def get_eye_parts(parts, left = True):# 目部分の座標を求める
    if left:
        eye_parts = [
                parts[36],
                min(parts[37],parts[38], key=lambda x: x.y),#parts[37].yとparts[38].yの大きいほう
                max(parts[40],parts[41], key=lambda x: x.y),
                parts[39],
               ]
    else:
        eye_parts = [
                parts[42],
                min(parts[43],parts[44], key = lambda x: x.y),
                max(parts[46],parts[47], key=lambda x: x.y),
                parts[45],
               ]
    return eye_parts



def get_eye_image(img, parts, left = True): #カメラ画像と見つけた顔の座標から目の画像を求めて表示する
    if left:
        eyes = get_eye_parts(parts, True)
    else:
        eyes = get_eye_parts(parts, False)
    org_x = eyes[0].x
    org_y = eyes[1].y

    if is_close(org_y, eyes[2].y):
        return None
    eye = img[org_y:eyes[2].y, org_x:eyes[-1].x] #画像から瞳部分をトリミング　
    # img[top : bottom, left : right]
    # Pythonのリスト：マイナスのインデックスは最後尾からの順番を意味する  

    height = eye.shape[0]
    width = eye.shape[1]
    resize_eye = cv2.resize(eye , (int(width*5.0), int(height*5.0)))

    if left : 
        cv2.imshow("left",resize_eye)
        cv2.moveWindow('left', 50, 200)
    else :
        cv2.imshow("right",resize_eye)
        cv2.moveWindow('right', 350, 200)
    
    return eye

def get_eye_center(img, parts, left = True): #Partsから目のセンター位置を求めて、表示する
        if left:
            eyes = get_eye_parts(parts, True)
        else:
            eyes = get_eye_parts(parts, False) 

        x_center = int(eyes[0].x + (eyes[-1].x - eyes[0].x)/2)
        y_center = int(eyes[1].y + (eyes[2].y - eyes[1].y)/2)

        cv2.circle(img, (x_center, y_center), 3, (255,255,0), -1)
        return x_center, y_center

def get_pupil_location(img, parts, left = True):#Partsから瞳の位置を求めて表示する、その過程で目の二値化画像を表示
     if left:
            eyes = get_eye_parts(parts, True)
     else:
            eyes = get_eye_parts(parts, False)
     org_x = eyes[0].x
     org_y = eyes[1].y
     if is_close(org_y, eyes[2].y):
        return None
     eye = img[org_y:eyes[2].y, org_x:eyes[-1].x]
     _, threshold_eye = cv2.threshold(cv2.cvtColor(eye, cv2.COLOR_RGB2GRAY),30, 255, cv2.THRESH_BINARY_INV)#第一引数を無視して二値化
     
     height = threshold_eye.shape[0]
     width = threshold_eye.shape[1]
     resize_eye = cv2.resize(threshold_eye , (int(width*5.0), int(height*5.0)))

     if left : 
        cv2.imshow("left_threshold",resize_eye)
        cv2.moveWindow('left_threshold', 50, 300)
     else :
        cv2.imshow("right_threshold",resize_eye)
        cv2.moveWindow('right_threshold', 350, 300)
     
     center = get_center(threshold_eye)

     if center:
         cv2.circle(img, (center[0] + org_x, center[1] + org_y), 3, (255, 0, 0), -1)
         return center[0] + org_x, center[1] + org_y
     return center


    #center = get_center(eye)
    #if center:
    #    return center[0] + org_x, center[1] + org_y
    #return center





cap = cv2.VideoCapture(0)
while True:
   ret, frame = cap.read() #Videoを読み込む
   # ここに処理を追加していく　----
   dets = detector(frame[:, :, ::-1])
   if len(dets) > 0:
       parts = predictor(frame, dets[0]).parts()
       
       left_eye_image =get_eye_image(frame,parts, True)
       right_eye_image = get_eye_image(frame,parts,False)
       left_eye_center = get_eye_center(frame,parts, True)
       right_eye_center = get_eye_center(frame,parts, False)
       left_pupil_location = get_pupil_location(frame, parts, True)
       Right_pupil_location = get_pupil_location(frame, parts, False)

       cv2.imshow("me", frame)
       #p(frame, parts, (left_eye, right_eye))
   # ここまで　----

   if cv2.waitKey(1) == 27: #キーボードが何か入力されたら
       break
cap.release()
cv2.destroyAllWindows()