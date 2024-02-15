import grpc
import requests
from bencherscaffold.bencher_pb2 import BenchmarkRequest
from bencherscaffold.bencher_pb2_grpc import BencherStub

if __name__ == '__main__':
    stub = BencherStub(
        grpc.insecure_channel(f"127.0.0.1:{50051}")
    )

    print(stub)

    headers = {
        'Authorization': 'token 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',
        'Accept'       : 'application/vnd.github.v3.raw',
    }

    response = requests.get(
        'https://raw.githubusercontent.com/LeoIV/bencher/master/BencherServer/bencherserver/benchmark-registry.json',
        headers=headers
    )

    registry = response.json()

    for benchmarkname, properties in registry.items():
        dimensions = properties['dimensions']

        print(f"benchmarkname: {benchmarkname}, dimensions: {dimensions}")

        res = stub.EvaluatePoint(
            BenchmarkRequest(
                benchmark=benchmarkname,
                point={'values': [1] * dimensions}
            )
        )
        print(res)
