# Project概要
- OpenCV・Pythonの練習と今後の心理学研究での視線分析の必要を兼ねて、OpenCVで視線追跡することを目指す


# 瞳の位置を検知してカメラ映像に投影する
## 環境作成
### OpenCVのインストール
- pythonのOpencvを下記コマンドをコマンドプロンプトから入力してインストールする<br>"pip install opencv–python"
- Pythonの対話型実行環境を実行してOpenCVのライブラリcv2が利用できるかをチェック

- 対話型実行環境が起動されると「>>>」とプロンプトが表示されるので"import cv2"と入力。エラーが出なければinstallできている。
### dlibのインストール
dlibとはC++の機械学習・画像解析用ライブラリ
- dlibのinstallにはCMakeのインストールが必要
- Cmakeのインストール→ https://qiita.com/East_san/items/b8ebc34dad226865899a
- dlibのインストール→ https://qiita.com/Kurobani/items/fd84fd941f527c46ab98

## 学習済みモデルのダウンロード
 - 顔器官の取得に学習が必要なため、学習済みのモデルをダウンロードする
 　http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
 - 学習済みモデルはプログラムと同じ階層に置く。

 ## 下記ページを参考に顔器官の表示を行ってみる
 - https://cppx.hatenablog.com/entry/2017/12/25/231121
 ### 嵌ったポイント
 - 検出器の読み込みを相対パスで行うと、ファイルが読み込めない下記エラーが出たので絶対パスにした。ところうまくいった
  RuntimeError: Unable to open shape_predictor_68_face_landmarks.dat
 
 ```
path = '/Users/GakutoSasabe/Desktop/Research/OpencvEyetracking/shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(path)
```
## 瞳座標の取得
目の部分から黒い部分を抜き出してその重心を瞳にする
### dlibの座標の順番
http://mizutanikirin.net/unity-dlib-facelandmark-detector%E3%81%A7%E9%A1%94%E8%AA%8D%E8%AD%98

### OpenCVの二値化について
https://pystyle.info/opencv-image-binarization/

### 二値化した画像の重心を求める方法
https://cvtech.cc/pycvmoment/

# 瞳の位置からどの方向を向いているか推定する
## 参考文献
- こちらの記事を参考としました。　https://www.remma.net/?p=37
- こちらも　https://qiita.com/sassa4771/items/fbfb0012744350cf4d93


### やりたいこと
#### 表示要件
 - カメラで自分の顔が映り、瞳の部分が点で光る
 - 目の部分が切り出されてWindowに映る
 - 二値化された目の画像もwindowに移る
#### 機能要件
 - 瞳が上下左右どちらの方向を向いているか表示される
 - 左右の目の中心に対しての瞳の座標が表示される

### タスク
#### 1.目の画像の取得
 - dlibで左右の目の座標を取得する →get_eye_parts関数
 - 目の座標から右目・左目の画像を取得する →get_eye_image関数

#### 2.瞳の座標の取得 get_pupil_location関数
 - 左右の目の画像をそれぞれ二値化する→get_pupil_location関数
 - 二値化した画像から左右の目の重心を求める（これを瞳の座標とする)→get_pupil_location関数
 - 瞳の座標に点を描画する→get_pupil_location関数
#### 3.目の中央に対しての瞳座標の可視化
 - 1.で求めた目の画像から目の中央の座標取得する →get_eye_center関数
 - 中央座標と、2.で求めた瞳の座標から「目の中央に対しての瞳のx,y座標」を求める →culculate_relative_pupil_position関数
 - 瞳のx,y座標を表示する→culculate_relative_pupil_position関数
#### 4.目の領域の分割と目線方向の表示
 - 1.で取得した右目、左目の領域を左右に三等分して左(Left)、右(Right)、中央(straight)の領域を求める →culculate_direction関数
 - 1.で取得した右目、左目の領域を上下に三等分して上(UP)、下(Down)、中(Middle)の領域を求める →culculate_direction関数
 - 3.で取得した瞳の座標と領域を比較して、目がどちらの方向を向いているか推定する →culculate_direction関数
 - 右目・左目の向いている方向を表示する
  →culculate_direction関数

### できたもの
https://youtu.be/qzXtZFp7HQU
- 目の中の青点：検出された瞳の位置
- 目の中の水色点：dlibで検出された目の中央位置
- 画面下座標：目の中央位置に対しての瞳の相対座標

### 感想
- OpenCVを初めて使ったがめっちゃ便利
- 心理学研究にはかなり有用なツールになりそう
- 目の画像を二値化して、黒目部分の重心を瞳の位置とするという単純なやり方でもまぁまぁ精度は出る
- ただ、周囲の明るさにかなり影響を受けるので、二値化の閾値の調整が環境変更のたびに必要かも
- 作り終わってから知ったのがどうやら目の画像にハフ変換をかけて、円を検出するというやり方が主流らしいので
そっちも時間があれば試してみたい

### ソース
https://github.com/gakutosasabe/OpenCVEyeTracking