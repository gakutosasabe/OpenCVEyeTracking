# Project概要
- OpenCV・Pythonの練習と今後の心理学研究での視線分析の必要を兼ねて、OpenCVで視線追跡することを目指す

# スケジュール
- 1月中に目の位置をアプリで表示する


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
![](2022-01-17-23-05-51.png)

### OpenCVの二値化について
https://pystyle.info/opencv-image-binarization/

### 二値化した画像の重心を求める方法
https://cvtech.cc/pycvmoment/

# 瞳の位置からどの方向を向いているか推定する
## 参考文献
- 松田君の記事を参考とする　https://www.remma.net/?p=37
- https://qiita.com/sassa4771/items/fbfb0012744350cf4d93

## 演算子の意味
-  //	 a//b	 aをbで割った商の整数値

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
 - dlibで左右の目の座標を取得する get_eye_parts関数
 - 目の座標から右目・左目の画像を取得する get_eye_image関数

#### 2.瞳の座標の取得 get_pupil_location関数
 - 左右の目の画像をそれぞれ二値化する; 
 - 二値化した画像から左右の目の重心を求める（これを瞳の座標とする)
 - 瞳の座標に点を描画する
#### 3.目の中央に対しての瞳座標の可視化
 - 1.で求めた目の画像から目の中央の座標取得する get_eye_center
 - 中央座標と、2.で求めた瞳の座標から「目の中央に対しての瞳のx,y座標」を求める
 - 瞳のx,y座標を表示する
#### 4.目の領域の分割と目線方向の表示
 - 1.で取得した右目、左目の領域を左右に三等分して左(Left)、右(Right)、中央(straight)の領域を求める
 - 1.で取得した右目、左目の領域を上下に三等分して上(UP)、下(Down)、中(Middle)の領域を求める
 - 3.で取得した瞳の座標と領域を比較して、目がどちらの方向を向いているか推定する
 - 右目・左目の向いている方向を表示する
