from __future__ import print_function

from datetime import datetime, timedelta
import logging
from multiprocessing import Process

import grpc
import loadtester_pb2
import loadtester_pb2_grpc


def call(token: str, block: int) -> None:
    logging.basicConfig()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = loadtester_pb2_grpc.LoadTesterStub(channel)
        request = loadtester_pb2.Request(token=token, block=block)
        print(f"Client send: {request.token=} {request.block=}")
        start = datetime.now()
        response = stub.Call(request)
        delta = (datetime.now() - start) / timedelta(milliseconds=1)
        print(f"Client recv: {response.token=} {delta=}")


def main() -> None:
    args_list = [
        ("1-1", 1),
        ("1-2", 1),
        ("1-3", 1),
        ("1-4", 1),
        ("1-5", 1),
        ("1-6", 1),
        ("1-7", 1),
        ("1-8", 1),
    ]
    ps = [Process(target=call, args=args) for args in args_list]

    start = datetime.now()
    [p.start() for p in ps]
    [p.join() for p in ps]
    delta = (datetime.now() - start) / timedelta(milliseconds=1)
    print(f"Elapsed: {delta=}")


if __name__ == "__main__":
    main()
