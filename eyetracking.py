import dlib
import cv2

detector = dlib.get_frontal_face_detector()
path = '/Users/GakutoSasabe/Desktop/Research/OpencvEyetracking/shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(path)

def is_close(y0,y1): #目が閉じているか判定する関数
    if abs(y0 - y1) < 10:
        return True
    return False

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