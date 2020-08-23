# Django 日志

### 日志模块的配置

###### 格式器formatter

用于配置log的格式，沿用了python里面的格式属性

* asctime 时间
* threadName 线程名称
* thread 线程id
* pathname 打印日志文件的路径
* funcName 打印日志的函数
* lineno 打印日志的代码行数
* levelname 打印日志的级别
* message 日志的具体信息

###### 过滤器filter

对日志进行过滤和匹配

###### 处理器handler

对日志进行处理，比如写进文件、打印屏幕等

常用处理器有 文件处理器、终端处理器

###### 日志实例logger

主要是在python代码中打印log日志的入口点

* 在打印的时候可以设置日志的级别：DEBUG、INFO、WARNINGE、ERROR、CRITICAL
* DEBUG、INFO、WARNINGE、ERROR、CRITICAL 的级别是层层递进的，就是说如果日志级别设置为DEBUG，那么 DEBUG 后面多有的日志类型都会被打印，如果设置为 INFO 那么 DEBUG 将不会被打印，如果设置为 WARNINGE 那么 DEBUG 和 INFO 将不会被打印

###### 日志模块的使用

~~~python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 日志
LOG_DIR = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    # 日志版本
    'version': 1,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(pathname)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s'
        }
    },
    # 日志过滤器
    'filters': {
        # 添加自定义的过滤器
        'test': {
            '()': 'ops.log_filters.TestFilter'
        }
    },
    # 日志处理器
    'handlers': {
        # 终端处理器
        'console_handler': {
            # handler的级别
            'level': 'INFO',
            # handler的类
            'class': 'logging.StreamHandler',
            # handler的格式器
            'formatter': 'standard'
        },
        'file_handler': {
            # handler的级别
            'level': 'DEBUG',
            # handler的类
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件路径、文件名
            'filename': os.path.join(LOG_DIR, 'backend.log'),
            # 文件最大存储值
            'maxBytes': 1024 * 1024 * 1024,
            # 保存的日志的备份的数量
            'backupCount': 5,
            # handler的格式器
            'formatter': 'standard',
            # 编码
            'encoding': 'utf-8'
        }
    },
    # 配置log实例
    'loggers': {
        'django': {
            'handlders': ['console_handler', 'file_handler'],
            'filters': ['test'],
            'level': 'DEBUG',
        }
    }
}
~~~

