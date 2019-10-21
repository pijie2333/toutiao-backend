import json
from flask import current_app

from models.user import User
from . import constants
# 构建缓存工具,查询mysql，查询redis，缓存数据的更新，返回数据，解决缓存击穿和雪崩问题。
# 需求：实现用户信息的缓存的工具

# 工具封装的思想：实现代码的封装，代码的复用；
# 类方法：类属性，类和实例可以调用，属性是固定，不会因为不同的类属性不同。
# 实例方法：实例属性，实例可以调用，属性是根据具体对象的不同，而不同。
# 静态方法：不需要操作类属性和实例属性，仅仅实现功能，可以定义静态方法。


class UserCache(object):

    def __init__(self,user_id):
        self.key = 'user:{}:profile'.format(user_id)
        self.user_id = user_id

    def query(self):
        r = current_app.redis_cluster
        # 4.1查询mysql，判断查询结果
        user = User.query.filter_by(id=self.user_id).first()
        # 4.2如果mysql没有，在redis中故意存储无效数据；解决缓存击穿问题！！
        if user is None:
            r.setex(self.key, constants.CacheNotExistsTTL.get_val(), '-1')
        # 4.3否则，把mysql查询结果缓存到redis中，解决缓存雪崩问题！！
        else:
            # 查询结果的对象转成字典数据，转成json，
            user_dict = dict(
                mobile=user.mobile,
                name=user.name,
                intro=user.introduction,
                photo=user.profile_photo
            )
            r.setex(self.key, constants.CacheUserTTL.get_val(), json.dumps(user_dict))
            return user_dict

    def get(self):
        # 步骤：查询redis----如果没有-----查询mysql
        # 1.查询redis分布式(核心初始化文件toutiao/init.py，59行)，根据self.key查询数据
        r = current_app.redis_cluster
        ret = r.get(self.key)
        # 2.判断查询结果是否存在
        # 3.如果redis存在数据
        if ret is not None:
            # 3.1需要进一步判断是否为有效数据，如果-1，返回无效数据，
            if ret == b'-1':
                return None
            # 3.2否则，把查询结果转成字典返回
            else:
                return json.loads(ret)
        # 4.如果redis中查询结果不存在
        else:
            ret = self.query()
            return ret


    def delete(self):
        r = current_app.redis_cluster
        r.delete(self.key)

    def exists(self):
        # 实现步骤：返回True或False
        # 1.查询redis，判断查询结果，如果redis有数据，进一步判断是否为有效数据，返回True或False
        r = current_app.redis_cluster
        ret = r.get(self.key)
        if ret is not None:
            if ret == b'-1':
                return False
            else:
                return True
        # 2.如果redis没有，查询mysql
        else:
            ret = self.query()
            if ret:
                return True
            else:
                return False


