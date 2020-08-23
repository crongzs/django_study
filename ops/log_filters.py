import logging


class TestFilter(logging.Filter):

    def filter(self, record):
        '''
        自定义过滤器
        :param record:  每条日志具体的内容
        :return:
        '''
        if '----' in record.msg:
            return False
        else:
            return True
