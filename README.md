# WRF traject
wrfoutの出力ファイルを用いて後方・前方流跡線解析を行い、点群形式のファイルに出力するツール。<br>
点群の可視化には[CloudCompare](https://www.danielgm.net/cc/)を用いることを想定してある。

## 使い方
1. pythonを用いて実行するため、pythonの必要なパッケージがインストールされていることを確認して下さい。
2. `config.py`に流跡線解析のための設定を記述してください。
3. `wrf_trajectory.py`を実行してください。
4. `mkpts.py`で点群形式のファイルを作成します。
5. CloudCompare等で流跡線および標高データが見れます。

## 必要なpythonパッケージ
- numpy
- netCDF4
- wrf-python
- geocat.f2py
- pandas
- matplotlib

## 注意点
1. 流跡線の計算には、時間・鉛直・水平面で風向・風速の内挿を行うことで空気塊を移動させている。このため、WRFの出力時間間隔が大きい場合は実際の流跡線と異なる可能性がある。
2. 現時点(2023.12)では領域外についても計算を行う仕様である。
