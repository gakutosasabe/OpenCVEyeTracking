import dlib
import cv2

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
    

def eye_point(img, parts, left = True): #引数は顔画像・顔器官画像・左目or右目（Trueで左目）
    if left:
        eyes = [
                parts[36],
                max(parts[37],parts[38], key=lambda x: x.y),#parts[37].yとparts[38].yの大きいほう
                min(parts[40],parts[41], key=lambda x: x.y),
                parts[39]
               ]
    else:
        eyes = [
                parts[42],
                max(parts[43],parts[44], key = lambda x: x.y),
                min(parts[46],parts[47], key=lambda x: x.y),
                parts[45],
               ]
    org_x = eyes[0].x
    org_y = eyes[1].y

    if is_close(org_y, eyes[2].y):
        return None
    eye = img[org_y:eyes[2].y, org_x:eyes[-1].x] #画像から瞳部分をトリミング　
    # img[top : bottom, left : right]
    # Pythonのリスト：マイナスのインデックスは最後尾からの順番を意味する
    _, eye = cv2.threshold(cv2.cvtColor(eye, cv2.COLOR_RGB2GRAY),30, 255, cv2.THRESH_BINARY_INV)#第一引数を無視して二値化
    #アンダーバーはReturnを無視する

    center = get_center(eye)
    if center:
        return center[0] + org_x, center[1] + org_y
    return center

    
    





cap = cv2.VideoCapture(0)
while True:
   ret, frame = cap.read() #Videoを読み込む
   # ここに処理を追加していく　----
   dets = detector(frame[:, :, ::-1])
   if len(dets) > 0:
       parts = predictor(frame, dets[0]).parts()
       img = frame * 0
       for i in parts:
           cv2.circle(img, (i.x, i.y), 3, (255, 0, 0), -1)

       cv2.imshow("me", img)
   # ここまで　----

   if cv2.waitKey(1) == 27: #キーボードが何か入力されたら
       break
cap.release()
cv2.destroyAllWindows()