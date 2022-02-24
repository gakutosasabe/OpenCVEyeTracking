# Project概要
- Pythonで作った視線分析のアプリを研究で使いやすくするためにGUIをつけて、視線位置情報のCSVへの吐き出しや、動画からの瞳位置情報の検出などを行う
# 要件定義
- UIから瞳位置情報を記録するCSVファイルの指定と、記録開始・停止が行える
- UIから読み込む動画ファイルの指定と、瞳位置情報を記録するCSVファイルの指定が行える。
- 上記に加えて、解析後の動画ファイル（瞳位置が動画内にポイントされているもの）が出力されているとなおいい
- 現在の瞳位置情報がリアルタイムでグラフに表示される
# 実装
## PythonでGUIを使う
- Tkinterを使ってPythonでGUIを作る
### Tkinterとは
- PythonでGUIを組むことのできるツールキット
###　使い方
#### tkinterのimport
- GUIを使いたいpythonスクリプト中でtkinterをimportするだけ
```
import tkinter as tk
```
## CSVに瞳位置情報を吐き出す
### 要件定義
- A行はそれぞれの列の説明
- A列にタイムスタンプ
- B~E列に右瞳・左瞳の相対位置のX座標、Y座標を出力する。
https://www.delftstack.com/ja/howto/python/python-append-to-csv/
- "E"キーを押すと、pupil_locate.csvに値が出力される
### 起きた問題
- 標準のcsvモジュールで吐き出したらアプリが重くなってしまった
### 対策
- 毎サイクル一行ずつ書き出しているからだと考えられるので"E"キーを押したらアプリ起動から今まで取った値を一括で書き込むようにする
- csvに複数行書き込む
    - https://algorithm.joho.info/programming/python/csv-writerows/



### 参考資料
- https://qiita.com/sassa4771/items/865ce07eaa6cf8e073c8
- https://nnahito.gitbooks.io/tkinter/content/
- tkinterのMainloopについて解説<br>
https://daeudaeu.com/mainloop/
## 動画から検出を行う
### 参考資料
https://kivantium.hateblo.jp/entry/2015/04/05/223841