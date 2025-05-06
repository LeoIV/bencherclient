import random

import requests
from bencherscaffold.client import BencherClient
from bencherscaffold.protoclasses.bencher_pb2 import PointType

if __name__ == '__main__':

    client = BencherClient()

    headers = {
        'Authorization': 'token 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',
        'Accept': 'application/vnd.github.v3.raw',
    }

    response = requests.get(
        'https://raw.githubusercontent.com/LeoIV/bencher/master/BencherServer/bencherserver/benchmark-registry.json',
        headers=headers
    )

    registry = response.json()

    for benchmarkname, properties in registry.items():
        dimensions = properties['dimensions']
        benchmark_type = properties['type']
        # types can be PURELY_CONTINUOUS, PURELY_BINARY,PURELY_CATEGORICAL,PURELY_ORDINAL_REAL,PURELY_ORDINAL_INT, MIXED (lower case)
        # but we only support PURELY_CONTINUOUS, PURELY_BINARY,PURELY_CATEGORICAL,PURELY_ORDINAL_INT
        # create point type

        # if dimension is None, sample one between 1 and 10
        if dimensions is None:
            dimensions = random.randint(1, 10)

        match benchmark_type:
            case 'purely_continuous':
                point_type = PointType.CONTINUOUS
                values = [0.5] * dimensions
            case 'purely_binary':
                point_type = PointType.BINARY
                values = [0] * dimensions
            case 'purely_categorical':
                point_type = PointType.CATEGORICAL
                values = [0] * dimensions
            case 'purely_ordinal_int':
                point_type = PointType.PURELY_ORDINAL_INT
                values = [0] * dimensions

        client.evaluate_point(
            benchmark_name=benchmarkname,
            point=values,
            type=point_type
        )
