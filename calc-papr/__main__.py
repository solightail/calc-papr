""" __main__ priting python """
import sys
import argparse
import traceback
from .core import program

def main() -> None:
    """ main function printing python """

    if len(sys.argv) == 1:
        # コマンドライン引数が無かった場合はヘルプメッセージを出力
        args.parse_args(["-h"])
        sys.exit(0)

    # エラー確認
    try:
        exit_code = program(args)
        sys.exit(exit_code)

    except ImportError as error:
        stack_trace: str = traceback.format_exc()

        if args.stacktrace:
            print("{:=^30}".format(" STACK TRACE "))
            print(stack_trace.strip())

        else:
            sys.stderr.write(f"{error.name}: {error.msg}\n")
            sys.exit(1)

if __name__ == "__main__":
        # コマンドライン引数リストの取得
    parse = argparse.ArgumentParser(prog='repapr')

    parse.add_argument('tones', type=int, help='number of tones')
    parse.add_argument('model', type=str, choices=['all0', 'narahashi', 'newman', 'frank', 'random', 'manual', 'manual_pi'], help='model to use')
    parse.add_argument('-k', type=float, nargs='*', default=None, help='input manual theta_k_values')
    parse.add_argument('-df', type=float, nargs='?', default=1.0, help='delta frequency')
    parse.add_argument('-dt', type=float, nargs='?', default=0.0001, help='delta time')
    parse.add_argument('-a', type=float, nargs='?', default=1.0, help='amplitude of each tone')
    parse.add_argument('-o', '--filename', type=str, nargs='?', default=None, help='svg / csv / txt file output file name')
    parse.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')
    parse.add_argument("--stack-trace", dest="stacktrace", action="store_true", help="Display the stack trace when error occured.")
    args = parse.parse_args()

    # ファイルパス・ファイル名をしていしていない場合
    if args.filename is None:
        if args.d == 0:
            args.path = f'./out/{args.model}/'
            args.filename = f'N{args.tones}_{args.model}'
        else:
            args.path = f'./out/{args.model}/'
            args.filename = f'N{args.tones}_{args.model}_{args.d}'
    else:
        args.path = f'./out/'
        args.filename = f'{args.filename}'

    # 位相決定をマニュアルにしている場合、パラメータがあるかの確認を行う
    if args.model == 'manual' or args.model == 'manual_pi':
        if args.k is None:
            raise argparse.ArgumentError(None, "If using the manual model, enter theta_k_values.")
        if len(args.k) != args.tones:
            raise argparse.ArgumentError(None, "The entered theta_k_values don\'t match the tones.")
        args.k = tuple(args.k)

    main()
