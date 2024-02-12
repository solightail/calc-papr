""" Class Calculation PAPR printing python """
import os
import math
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pandas as pd

class Formula:
    """ Formula used to calculate PAPR """
    def __init__(self, tones: int, del_freq: float, amp: float) -> None:
        # 引数より
        self.tones: int = tones
        self.del_freq: float = del_freq
        self.amp: float = amp

    def calc_p0t(self, time, theta_k_values):
        """ P_0(t) 計算 """
        # 計算プログラム自体は ChatGPT に丸投げし、修正を加えたもの

        # 変数定義 (numpyにて公差を求め、2次元配列として定義)
        # np.arange で指定した上限値は未満となることに注意！
        k_values: np.ndarray[int] = np.arange(1, self.tones)    # k=1 -> k=N-1
        l_values: np.ndarray[int] = np.arange(2, self.tones+1)  # l=2 -> l=N
        l_values_h: np.ndarray[int] = l_values[:, np.newaxis]   # l_valuesを2次元に変形

        # cos 計算 (2重和に向けて2次元配列のまま計算を行っている)
        # np.take -> 与えられたインデックスに従って配列から要素を選択する関数
        # l_values_h - 1 と k_values - 1 は配列から選択するための数値調整
        cos_values = np.cos(2 * np.pi * (l_values_h - k_values) * self.del_freq * time
                            + np.take(theta_k_values, l_values_h - 1)
                            - np.take(theta_k_values, k_values - 1))

        # 2重和計算
        p0t = np.sum(cos_values * (l_values_h > k_values))
        return p0t

    def calc_ept(self, p0t):
        """ 瞬時包絡線電力 計算 """
        ept = self.tones * self.amp**2 + 2 * self.amp**2 * p0t
        return ept

    def calc_papr_w(self, p0t):
        """ PAPR（Peak-to-Average-Power-Ratio）計算 """
        papr_w = 1 + ((2 * p0t) / self.tones)
        return papr_w

class FList:
    """ Formula クラスを移譲して、各式より求められる値をリストにまとめる """
    def __init__(self, formula: Formula, del_time: float) -> None:
        self.del_time = del_time
        self.formula = formula

    def calc_list(self, theta_k_values):
        """ 各式の計算結果をリストへ """
        # 計算速度向上のため、numpy より公差を使用して計算を行う
        # 2次元配列にしておかないと cos_values を計算できないことに注意する
        time_points: np.ndarray = np.arange(0.0, 1.0 + self.del_time, self.del_time)

        # 動的型付けを用いるため、型定義を行わないこと！
        time_values = time_points.tolist()
        # 時間については ndarray で計算できる代物でないため、内包表現を用いて計算を行う
        p0t_values = tuple(self.formula.calc_p0t(i, theta_k_values) for i in time_points)
        p0t_array = np.array(p0t_values)
        ept_values = tuple(self.formula.calc_ept(p0t_array).tolist())
        papr_w_values = tuple(self.formula.calc_papr_w(p0t_array).tolist())
        return time_values, p0t_values, ept_values, papr_w_values

class FMax:
    """ FList クラスを移譲して、最大値を求める """
    def __init__(self, flist: FList, theta_k_values) -> None:
        self.flist = flist
        self.time_values, self.p0t_values, self.ept_values, self.papr_w_values = flist.calc_list(theta_k_values)

    def calc_max(self) -> dict[str, float]:
        """ 各値の最大値を求めて、辞書に挿入 """
        # 時間から各値を求めるための辞書作成
        papr_times: dict[float, float] = dict(zip(self.papr_w_values, self.time_values))
        times_ept: dict[float, float] = dict(zip(self.time_values, self.ept_values))

        # PAPR最大値の算出
        max_papr_w: float = np.max(self.papr_w_values)
        max_papr_db: float = 10 * math.log10(max_papr_w)
        max_time: float = papr_times.get(max_papr_w)
        max_ept: float = times_ept.get(max_time)

        # 各最大値の辞書作成
        max_dict: dict[str, float] = {"papr_w": max_papr_w, "papr_db": max_papr_db,
                                      "time": max_time, "ept": max_ept}
        return max_dict

class FContext:
    """ プロット画像 / CSVファイル / テキスト 出力を行う """
    def __init__(self, fmax: FMax, path: str, filename: str, theta_k_cli: tuple[str]) -> None:
        # fmaxインスタンスより各リスト取得
        self.tones = fmax.flist.formula.tones
        self.time_values = fmax.time_values
        self.p0t_values = fmax.p0t_values
        self.ept_values = fmax.ept_values
        self.papr_w_values = fmax.papr_w_values

        # 最大値計算
        self.max_dict = fmax.calc_max()

        # その他
        self.path = path
        self.filename = filename
        self.theta_k_cli = theta_k_cli

        # 表示テキスト
        self.txt: str = f'time: {self.max_dict.get("time")} s / EP(t): {self.max_dict.get("ept")} W\nPAPR: {self.max_dict.get("papr_w")} W / {self.max_dict.get("papr_db")} dB\n'

    def mkdir(self) -> None:
        os.makedirs(self.path, exist_ok=True)

    def plot(self) -> None:
        """ 包絡線描画 """

        # ピーク値取得
        # 1) 谷を取得するには、tupleやlistではできないため、arrayに変換している
        array_ept_values = np.array(self.ept_values)
        upper_peaks, _ = find_peaks(array_ept_values, distance=10, plateau_size=1)
        lower_peaks, _ = find_peaks(-array_ept_values, distance=10, plateau_size=1)

        # 2) find_peaks は t = 0 にピークがある場合を考慮していない。
        #    1周期でこれを判断することは不可能であるため、2周期分で判断をし、1周期分に戻す作業を行う。
        two_ept_values = np.concatenate([array_ept_values, array_ept_values[1:]])
        two_upper_peaks, _ = find_peaks(two_ept_values, distance=10, plateau_size=1)
        two_lower_peaks, _ = find_peaks(-two_ept_values, distance=10, plateau_size=1)
        period: int = len(self.ept_values)-1
        if (period in two_upper_peaks):
            upper_peaks = np.concatenate([[0], upper_peaks, [period]])
        if (period in two_lower_peaks):
            lower_peaks = np.concatenate([[0], lower_peaks, [period]])

        # 3) 最大値と準最大値のみを考慮する
        upper_peaks_heights = np.take(array_ept_values, upper_peaks)
        max2_reverse_upper_peaks = upper_peaks[np.argsort(upper_peaks_heights)][-2:]
        lower_peaks_heights = np.take(array_ept_values, lower_peaks)
        max2_reverse_lower_peaks = lower_peaks[np.argsort(lower_peaks_heights)][:2]

        up1t = np.take(self.time_values, max2_reverse_upper_peaks[1])
        up1h = np.take(array_ept_values, max2_reverse_upper_peaks[1])
        up2t = np.take(self.time_values, max2_reverse_upper_peaks[0])
        up2h = np.take(array_ept_values, max2_reverse_upper_peaks[0])
        lo1t = np.take(self.time_values, max2_reverse_lower_peaks[0])
        lo1h = np.take(array_ept_values, max2_reverse_lower_peaks[0])
        lo2t = np.take(self.time_values, max2_reverse_lower_peaks[1])
        lo2h = np.take(array_ept_values, max2_reverse_lower_peaks[1])

        # プロット
        plt.plot(self.time_values, self.ept_values, label="EP(t)")
        # ピーク値表示
        #plt.plot(np.take(self.time_values, upper_peaks), np.take(self.ept_values, upper_peaks), "x", label="Upper Peak")
        #plt.plot(np.take(self.time_values, lower_peaks), np.take(self.ept_values, lower_peaks), "x", label="Lower Peak")
        #plt.plot(up1t, up1h, "x", label="1st UP")
        #plt.plot(up2t, up2h, "x", label="2nd UP")
        #plt.plot(lo1t, lo1h, "x", label="1st LP")
        #plt.plot(lo2t, lo2h, "x", label="2nd LP")
        # MSE表示
        #plt.fill_between(self.time_values, self.ept_values, self.tones, fc="blue", alpha=0.2)
        plt.xlabel('Time')
        plt.xlim(0, 1)
        plt.xticks([0, 0.5, 1], ['0', 'T/2', 'T'])
        plt.ylabel('EP(t)')
        plt.ylim(0, )
        #plt.legend() #凡例表示
        plt.grid(True)
        plt.savefig(f'{self.path}{self.filename}.svg', format='svg')

    def display(self) -> None:
        """ 計算結果をCLIへ出力 """
        print(self.txt)

    def save(self) -> None:
        """ 計算結果をcsv/txtファイルへ出力 """
        # csvファイルへ出力
        data: pd.DataFrame = pd.DataFrame({
            'Time [s]': self.time_values,
            'P0(t)': self.p0t_values,
            'EP(t) [W]': self.ept_values,
            'PAPR [W]': self.papr_w_values
        })
        data.to_csv(f'{self.path}{self.filename}.csv', index=False)

        # txtファイルへ出力
        with open(f'{self.path}{self.filename}.txt', encoding="utf-8", mode='w') as file:
            if len(self.theta_k_cli) == 0:
                file.write(self.txt)
            else:
                file.write(self.txt)
                for i, value in enumerate(self.theta_k_cli):
                    if i == 0:
                        file.write('\n')
                    file.write(f'{value}\n')
