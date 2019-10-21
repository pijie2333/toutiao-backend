# -*- coding: utf-8 -*-
from flask import current_app

from qiniu import Auth, put_file, etag,put_data
import qiniu.config

def upload(data):
    #需要填写你的 Access Key 和 Secret Key，每个同学使用自己的ak和sk
    access_key = current_app.config.get("QINIU_ACCESS_KEY")
    secret_key = current_app.config.get("QINIU_SECRET_KEY")

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间,需要手动创建
    bucket_name = current_app.config.get("QINIU_BUCKET_NAME")

    #上传后保存的文件名
    key = None

    #生成上传 Token，可以指定过期时间等,有效期单位秒
    token = q.upload_token(bucket_name, key, 360000)

    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    #
    # ret, info = put_file(token, key, localfile)
    # print(info)
    # 断言，key表示上传成功后的文件名称
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

    # f = open('./66.png','rb')
    # data = f.read()

    # data是需要上传的文件的二进制流
    ret,info = put_data(token,key,data)
    print("info=={}".format(info))
    return ret['key']
