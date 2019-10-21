# 导入flask-restful
from flask_restful import Resource,reqparse
# 导入Flask内置的对象
from flask import g,current_app

# 导入登录验证装饰器
from utils.decorators import login_required
# 导入参数校验的工具
from utils.parser import check_image
# 导入七牛云工具
from utils.oss_qiniu import upload
# 导入模型类
from models.user import User
# 导入数据库会话对象db
from models import db

# 上传头像接口
class PhotoResource(Resource):

    method_decorators = [login_required]

    def patch(self):
        # 实现步骤：
        # 1.用户登录验证装饰器，g.user_id
        user_id = g.user_id
        # 2.获取参数/提取参数/校验参数
        req = reqparse.RequestParser()
        req.add_argument('photo',type=check_image,required=True,location='files',help='photo type error')
        args = req.parse_args()
        photo = args.get("photo")
        # 3.读取图片文件，具有read和write方法的对象叫做文件对象
        image_data = photo.read()
        # 4.调用七牛云工具，图片上传
        try:
            image_name = upload(image_data)
        except Exception as e:
            # 记录上传失败的异常信息
            current_app.logger.error(e)
            return {'message':'upload failed'},500
        # 5.保存用户头像图片文件，mysql，根据用户id查询用户信息，保存用户头像
        try:
            user = User.query.filter_by(id=user_id).first()
            # User.query.filter(User.id==user_id).update({'profile_photo':image_name})
            user.profile_photo = image_name
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return {'message':'save photo failed'}
        # 6.返回图片的绝对地址
        photo_url = current_app.config.get("QINIU_DOMAIN") + image_name
        return {'photo_url':photo_url}



