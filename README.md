# Calcuration PAPR Program

### コマンドライン引数について

- **tones**: 波数・トーン数
  int型 (必須)
- **model**: 利用するモデル
  str型 (必須) [選択肢: all0, narahashi, newman, frank, random, manual, manual_pi]
- -k: theta_k のマニュアル入力
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

### 必須パッケージ
- numpy
- matplotlib
- pandas
- scipy

### 使用方法
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
python -m calc-papr all0 10
```
