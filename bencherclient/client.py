import argparse

from bencherscaffold.bencher_pb2 import BenchmarkRequest
from bencherserver.server import BencherServer


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-b', '--benchmark', type=str, required=True, help='The name of the benchmark to evaluate'
    )
    argparser.add_argument(
        '-p', '--point', nargs='+', type=float, required=True, help='The point to evaluate'
    )
    args = argparser.parse_args()

    server = BencherServer()
    server.register_stub(
        [
            'lasso-dna',
            'lasso-simple',
            'lasso-medium',
            'lasso-high',
            'lasso-hard'
        ], 50053
    )

    server.register_stub(
        [
            'mopta08'
        ], 50054
    )

    server.start()

    br = BenchmarkRequest(
        benchmark=args.benchmark,
        point={'values': args.point}
    )

    val = server.EvaluatePoint(br)
    print(val)
    server.stop()


if __name__ == '__main__':
    main()
