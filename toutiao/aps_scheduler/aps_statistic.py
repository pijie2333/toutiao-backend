

"""
需求：在toutiao/__init__.py文件中的定时任务模块，需要执行的数据修正的功能
步骤：
1、查询mysql，查询所有用户发布的文章数量
2、删除redis
3、把mysql查询结果写入redis
key = 'count:user:arts'
SQL:
select user_id,count(article_id) from news_article_basic where status=2 group by user_id;
+---------+-------------------+
| user_id | count(article_id) |
+---------+-------------------+
|       1 |             46141 |
|       2 |             46357 |
|       3 |             46187 |
|       5 |                25 |
+---------+-------------------+
ORM:
from sqlalchemy import func
db.session.query(Article.user_id,func.count(Article.id)).filter(Article.status==Article.STATUS.APPROVED).group_by(Article.user_id).all()

[<(1,46141)>,<2,46357>,<>]
zadd count:user:arts 46141 1 46357 2...


#############################
key = 'count:user:arts'
p = current_app.redis_master.pipeline()
p.delete(key)
for user_id,count in result:
    p.zadd(key,count,user_id)
p.execute()

"""
from cache import statistic as s


def __fix(tools_class):
    result = tools_class.query()
    tools_class.reset(result)


def fix_statistic(app):
    with app.app_context():
        # 1、调用工具类，查询所有用户发布的文章数量，修正数据
        # result = s.CountUserArticles.query()
        # s.CountUserArticles.reset(result)
        # # 查询用户粉丝数据
        # result = s.CountUserFans.query()
        # s.CountUserFans.reset(result)
        __fix(s.CountUserArticles)
        __fix(s.CountUserFans)


