from flask import current_app

from models import db
from models.news import Article
from models.user import Relation
from sqlalchemy import func

"""
持久存储设计：用户发布文章数量统计
key = 'count:user:arts'
count:user:arts   score(文章数量)   value(用户id)
                         10         1
                         20         2
实现步骤：利用redis主从，对集合的查询操作和自增操作。
1、查询redis中某个用户的文章数量
2、判断查询结果，如果存在，返回查询结果int()
3、返回0
4、实现数据的自增

"""

class Count(object):

    key = ''

    @classmethod
    def get(cls,user_id):
        # 因为是主从数据备份，主机器取不到数据，可以从从机器取数据
        # zscore count:user:arts wang
        try:
            ret = current_app.redis_master.zscore(cls.key,user_id)
        except Exception as e:
            current_app.logger.error(e)
            ret = current_app.redis_slave.zscore(cls.key,user_id)
        if ret:
            return int(ret)
        else:
            return 0

    # 文章数量增量，用户新发布一个文章，可以调用该功能
    @classmethod
    def incr(cls,user_id,increment=1):
        # zincrby count:user:arts 1 wang
        current_app.redis_master.zincrby(cls.key,increment,user_id)

    @classmethod
    def reset(cls,result):
        # 2、删除redis
        r = current_app.redis_master
        r.delete(cls.key)
        # 3、把mysql查询结果写入redis
        data_list = []
        for user_id, count in result:
            data_list.append(count)
            data_list.append(user_id)
        # *表示拆包，*args表示元祖和列表，**kwargs表示字典
        r.zadd(cls.key, *data_list)

    @staticmethod
    def query():
        pass


# 用户发布文章数量
class CountUserArticles(Count):
    key = 'count:user:arts'

    @staticmethod
    def query():
        return db.session.query(Article.user_id, func.count(Article.id)).filter(
            Article.status == Article.STATUS.APPROVED).group_by(Article.user_id).all()


# 用户关注
class CountUserFollowings(Count):
    key = 'count:user:followings'

# 用户粉丝
class CountUserFans(Count):
    key = 'count:user:fans'

    @staticmethod
    def query():
        return db.session.query(Relation.user_id,func.count(Relation.target_user_id)).filter(Relation.relation==Relation.RELATION.FOLLOW).group_by(Relation.user_id).all()

