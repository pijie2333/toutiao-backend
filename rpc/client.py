import grpc,time

import reco_pb2_grpc
import reco_pb2


# 模拟请求(喂养),
def feed_articles(stub):
    # 构建请求信息
    req = reco_pb2.UserRequest()
    req.user_id = '1001'
    req.channel_id = 2
    req.article_num = 5
    req.time_stamp = round(time.time() * 1000)
    resp = stub.user_recommend(req)
    print('resp={}'.format(resp))

# rpc客户端构建步骤：
def run():
    # 1.使用上下文管理器，指定连接的rpc服务器的主机和端口，创建channel对象
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        # 2.使用reco_pb2_grpc里面的stub工具，传入channel
        stub = reco_pb2_grpc.UserRecommendStub(channel)
        # 3.定义方法，传入stub工具，用来发送请求，解析响应
        feed_articles(stub)

if __name__ == '__main__':
    run()







