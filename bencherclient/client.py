from bencherscaffold.bencher_pb2 import BenchmarkRequest
from bencherserver.server import BencherServer


def main():
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
    server.start()

    br = BenchmarkRequest(
        benchmark='lasso-dna',
        point={'values': [1.0] * 180}
    )

    val = server.EvaluatePoint(br)
    print(val)
    server.stop()


if __name__ == '__main__':
    main()
