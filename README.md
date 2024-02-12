# Calcuration PAPR Program
PAPRの計算を行い、計算結果のまとめ（テキスト）・計算結果データ（CSV）・包絡線電力波形図（SVG）の出力を行います。  
初期位相は予め指定されたモデルと、マニュアル入力のどちらにも対応しています。

## コマンドライン引数について
- **tones**: 波数・トーン数  
  int型 (必須)
- **model**: 初期位相 決定モデル  
  str型 (必須) [選択肢: all0, narahashi, newman, frank, random, manual, manual_pi]
- -k: 初期位相のマニュアル入力  
  float型 (modelがmanualかmanual_piの場合に必ず使用)
- -df: 隣接するトーン間の周波数間隔  
  float型 (default: 1.0)
- -dt: 計算を行う時間間隔  
  float型 (default: 0.0001)
- -a: 各トーンの振幅  
  float型 (default: 1.0)
- -o: 演算結果 ファイルパスおよびファイル名  
  str型 (default: 条件に応じて指定)
- -v: バージョン

## モデルについて
- all0  
  各トーンの初期位相を全て0に設定
- narahashi  
  楢橋位相を使用して設定
- newman  
  Newman位相を使用して設定
- frank (experimental)  
  自己相関に優れ、相互相関の少ないFrankコードを用いて位相を設定  
  フーリエ変換を使用した手法で用いられるため、あくまで位相計算ができることを確認した試験実装
- random  
  乱数で位相を設定
- manual  
  手入力（rad）で位相を設定
- manual_pi  
  手入力（0~1の数値）で位相を設定（後に2πを掛けて計算をする）

## 使用方法
*各コマンドは参考程度で、各環境の状態に応じて実行してください。
1. venvで仮想環境を作成
```bash
python -m venv venv
venv\Scripts\activate.bat
```
2. 必須パッケージをインストール
```bash
python -m pip install --upgrade pip wheel
pip install numpy matplotlib pandas scipy
```
3. コマンドラインにて実行
```bash
python -m calc-papr 10 all0
```
