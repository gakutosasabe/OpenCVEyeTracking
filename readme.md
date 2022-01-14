# Project概要
- OpenCV・Pythonの練習と今後の心理学研究での視線分析の必要を兼ねて、OpenCVで視線追跡することを目指す

# スケジュール
- 1月中に目の位置をアプリで表示する

# 参考文献
- 松田君の記事を参考とする　https://www.remma.net/?p=37

# 手順
## 環境作成
### OpenCVのインストール
- pythonのOpencvを下記コマンドをコマンドプロンプトから入力してインストールする<br>"pip install opencv–python"
- Pythonの対話型実行環境を実行してOpenCVのライブラリcv2が利用できるかをチェック

- 対話型実行環境が起動されると「>>>」とプロンプトが表示されるので"import cv2"と入力。エラーが出なければinstallできている。
### dlibのインストール
- dlibのinstallにはCMakeとVisualStudioが必要
- Cmakeがinstallできん・・・・