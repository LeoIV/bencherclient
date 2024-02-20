import time

import grpc
import requests
from bencherscaffold.bencher_pb2 import BenchmarkRequest
from bencherscaffold.bencher_pb2_grpc import BencherStub

N_RETRIES = 5

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
        for n_retry in range(N_RETRIES):
            try:
                res = stub.evaluate_point(
                    BenchmarkRequest(
                        benchmark=benchmarkname,
                        point={'values': [1] * dimensions}
                    )
                )
                print(res)
                break
            except Exception as e:
                if n_retry < N_RETRIES - 1:
                    print(f'error: {e}')
                    # sleep for 5 seconds
                    time.sleep(5)
                else:
                    print(f'error: {e}')
                    raise e
