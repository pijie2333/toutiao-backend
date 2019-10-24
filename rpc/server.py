import grpc,time
from concurrent.futures import ThreadPoolExecutor

# 此处仅仅是pycharm的提示信息，不代表无法导入
import reco_pb2_grpc
import reco_pb2

# 可以自定义服务类，继承自reco_pb2_grpc里的UserRecommendServicer
class UserRecommendServicer(object):
    def user_recommend(self, request, context):
        # 接收请求，request不是Flask请求上下文对象
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp = request.time_stamp

        # 返回响应,后续需要对接推荐系统，获取推荐的文章列表，现在模拟推荐
        # 实例化文章对象
        resp = reco_pb2.ArticleResponse()
        resp.exposure = 'exposure params'
        resp.time_stamp = round(time.time() * 1000)
        # 默认返回的文章使用article_num
        data_list = []
        for i in range(article_num):
            article = reco_pb2.Article()
            article.article_id = i + 1
            article.track.click = 'click params {}'.format(i+1)
            article.track.collect = 'collect params {}'.format(i+1)
            article.track.share = 'share params {}'.format(i+1)
            article.track.read = 'read params {}'.format(i+1)
            data_list.append(article)
        resp.recommends.extend(data_list)
        return resp

def serve():
    # 步骤：
    # 1.定义rpc服务器,以线程池的方式运行
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    # 2.给服务器添加服务方法,第一个参数表示服务的对象，第二个参数表示grpc服务器对象
    reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)
    # 3.绑定主机和端口
    server.add_insecure_port('127.0.0.1:8888')
    # 4.启动服务器，默认非阻塞运行，需要开启死循环，让其阻塞
    server.start()
    while True:
        time.sleep(3)
    pass


if __name__ == '__main__':
    serve()




