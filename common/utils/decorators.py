from flask import g, current_app
from functools import wraps
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError


from models import db



# 实现登录验证装饰器
def login_required(f):
    # 装饰器默认情况下，会修改被装饰的函数的名称。
    # wraps的作用：让被装饰器函数的函数的属性不发生变化。
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 需要限制用户携带的只能token，不能是refresh_token
        if g.user_id and g.refresh is False:
            return f(*args,**kwargs)
        else:
            return {'message':'token error'},403
    # wrapper.__name__ = f.__name__
    return wrapper
















def set_db_to_read(func):
    """
    设置使用读数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)
    return wrapper


def set_db_to_write(func):
    """
    设置使用写数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)
    return wrapper


