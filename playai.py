import sys
from aidriver import run_ai, run_best_ai


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_best_ai()
    else:
        run_ai(sys.argv[1:])
