""" core priting python """
import sys
sys.path.append('./modules/algorithms.py')
from .modules import algorithms
from .modules import calc

def program(args):
    """ program function """
    # アルゴリズム選択
    match args.model:
        case 'all0':
            strategy = algorithms.All0(args.tones)
        case 'narahashi':
            strategy = algorithms.Narahashi(args.tones)
        case 'newman':
            strategy = algorithms.Newman(args.tones)
        case 'frank':
            strategy = algorithms.Frank(args.tones)
        case 'random':
            strategy = algorithms.Random(args.tones)
        case 'manual':
            strategy = algorithms.Manual(args.tones, args.k)
        case 'manual_pi':
            strategy = algorithms.ManualPi(args.tones, args.k)

    # theta_k 計算
    algo_context = algorithms.AContext(strategy)
    theta_k_values: tuple[float] = algo_context.calc_algo()
    theta_k_cli: tuple[str] = algo_context.display()

    # PAPR 計算
    formula = calc.Formula(args.tones, args.df, args.a)
    flist = calc.FList(formula, args.dt)
    fmax = calc.FMax(flist, theta_k_values)
    formula_context = calc.FContext(fmax, args.path, args.filename, theta_k_cli)
    formula_context.mkdir()
    formula_context.plot()
    formula_context.display()
    formula_context.save()

    return sys.exit()
