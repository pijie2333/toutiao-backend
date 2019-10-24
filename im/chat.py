from server import sio
import time

# 构建即时通讯聊天事件的客户端
# 1、连接后默认的执行的事件
@sio.on('connect')
def on_connect(sid,environ):
    # 连接后的客户端信息进行输出
    print('sid=={},environ=={}'.format(sid,environ))
    # 连接后，默认回复的消息内容
    msg_data = {
        'message':'hello!!',
        'time_stamp':int(time.time() * 1000)
    }
    # 发送消息给客户端
    sio.emit('message',data=msg_data,room=sid)

# 2、连接后的自定义的事件
@sio.on('flask')
def on_flask(sid,data):
    # 客户端发送的消息内容
    print('sid=={},data=={}'.format(sid,data))
    # 默认回复，后续可以对接NLP自然语言处理，或是图灵机器人
    msg_data = {
        'message':'I received your message {}'.format(data),
        'time_stamp':round(time.time() * 1000)
    }

    sio.send(data=msg_data,room=sid)


