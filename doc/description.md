# Calcuration PAPR Program

### コマンドライン引数について

- **tones**: 波数・トーン数
  int型 (必須)
- **models**: 利用するモデル
  str型 (必須) [選択肢: narahashi, newman, kaneoka, makihara]
- -d: 分割数
  int型 (default: 0 / モデルによっては使用しない)
- -df: 隣接するトーン間の周波数間隔
  float型 (default: 1.0)
- -dt: 計算を行う時間間隔
  float型 (default: 0.0002 / 金岡先輩のデフォルト値を流用)
- -a: 各トーンの振幅
  float型 (default: 1.0)
- -o: 演算結果 ファイル名
  str型 (default: N{arg.tones}\_{arg.model}\_{arg.d})
- -v: バージョン

### クラス図

```plantuml

Package Algorithm {
    abstract class Algorithm {
        tones: int
        calc()
    }

    class All0 {
        calc()
    }

    class Narahashi {
        calc()
    }

    class Newman {
        clac()
    }

    class Kaneoka {
        calc()
    }

    class Makihara {
        calc()
    }

    class AContext {
        _strategy: Algorithm
        theta_k_values: tuple[float]
        calc_algo()
        display()
    }

    All0 --|> Algorithm
    Narahashi --|> Algorithm
    Newman --|> Algorithm
    Kaneoka --|> Algorithm
    Makihara --|> Algorithm
    Algorithm o-- AContext
}

Package calc {
    class Formula {
        tones: int
        del_freq: float
        amp: float
        theta_k: tuple[float]

        calc_p0t(time)
        calc_ep_t(p0t)
        calc_papr_w(p0t)
    }

    class FList {
        formula: Formula
        del_time: float
        appends()
    }

    class FMax {
        flist: FList
        calc_max()
    }

    class FOut {
        flist: FList
        fmax: FMax
        filename: str

        plot()
        display()
        save()
    }

    Formula o-- FList
    FList o-- FMax
    FList o-- FOut
    FMax o-- FOut
}

```

