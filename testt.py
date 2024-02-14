import grpc
from bencherscaffold.bencher_pb2 import BenchmarkRequest
from bencherscaffold.bencher_pb2_grpc import BencherStub

if __name__ == '__main__':
    stub = BencherStub(
        grpc.insecure_channel(f"127.0.0.1:{50051}")
    )
    x = stub.EvaluatePoint(
        BenchmarkRequest(
            benchmark='mujoco-walker',
            point={'values': [1] * 102}
        )
    )
    print(x)