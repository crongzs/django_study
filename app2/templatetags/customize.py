from django import template

register = template.Library()

'''
过滤器最多能有两个参数
过滤器的第一个参数永远都是被过滤的那个参数，也就是竖线左边的参数

过滤器的注册方式一：
使用 register.filter() 将函数注册到 template 库中 成为一个模板过滤器
register.filter() 中的第一个参数是过滤器的名字，第二个参数是对应的要注册的函数名

过滤器的注册方式二：
使用装饰器 @register.filter 将函数注册到 template 库中 成为一个模板过滤器
@register.filter 默认会将函数的名字作为过滤器的名字进行注册，如果想要自定义过滤器的名字就想过滤器传递一个名字的字符串参数就可以了
'''


# 过滤器的注册方式一
def new_word(value1, value2):
    return value1 + value2


register.filter("str_joint", new_word)


# 过滤器的注册方式二 自定义过滤器的名称为 list_joint
@register.filter("list_joint")
def new_list(value1, value2):
    return [value1, value2]


# 过滤器的注册方式二 默认过滤器的名称为函数名称 hello
@register.filter
def hello(value1, value2=None):
    if value2:
        return value2 + value1
    else:
        return 'Hello ' + value1
