from django.core.signals import request_started, request_finished, got_request_exception
from django.dispatch import Signal

# 自定义信号
self_signal1 = Signal()
self_signal2 = Signal(providing_args=['request'])


# 定义信号处理函数
def my_callback(sender, **kwargs):
    print('This is a signal')


def request_log(sender, request, **kwargs):
    print(request.META)
    print(request.path)
    username = 'ku_rong'
    path = request.path
    data = dict(request.POST)
    request_data_log = "[{username}]:[{path}]:[{data}]".format(username=username, path=path, data=data)

    with open('request_data_log.txt', 'a') as fp:
        fp.write(request_data_log + '\n')


# 监听信号
self_signal1.connect(my_callback)
self_signal2.connect(request_log)
