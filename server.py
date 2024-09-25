from concurrent import futures
from datetime import datetime, timedelta
import logging

import grpc
import loadtester_pb2
import loadtester_pb2_grpc


class LoadTester(loadtester_pb2_grpc.LoadTesterServicer):
    def Call(self, request: loadtester_pb2.Request, context: grpc.ServicerContext) -> loadtester_pb2.Response:
        print(request.token, request.block)
        start = datetime.now()
        while (datetime.now() - start) / timedelta(seconds=1) < request.block:
            pass
        return loadtester_pb2.Response(token=request.token)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    loadtester_pb2_grpc.add_LoadTesterServicer_to_server(LoadTester(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
