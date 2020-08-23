from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
使用 User 模型 进行用户注册的时候 一定要使用 User.objects.create_user() 创建，不然密码 password 不会被加密
'''


# ----------- 扩展User模型 设置代理 -----------

# 给User模型做扩展，第一种方式做代理
class App13Person(User):
    # 如果模型是一个代理模型，那就不能在模型中添加新的属性
    # 好处时候可以自定义一些方法
    # App14Person.objects.all() 和 User.objects.all() 是等价的
    class Meta:
        proxy = True  # 告诉Django 这个模型是一个代理模型

    @classmethod
    def get_blacklist(cls):
        ''' 获取黑名单用户 '''
        return cls.objects.filter(is_active=False)


# ----------- 扩展User模型 一对一外键 -----------

# 给User模型做扩展，第二种创建一对一外键的模型

from django.dispatch import receiver  # receiver 是一个装饰器，可以接收某个信号，去执行相应的函数
from django.db.models.signals import post_save  # post_save 在调用 save()方法的时候它会发送信号


class App13UserExtension(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='extension')
    phone = models.CharField(max_length=11)


@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    '''

    :param sender: 发送者
    :param instance: 在调用 save() 方法时的实例
    :param created: 判断是否是新创建的
    :return:
    '''

    if created:
        # 如果是创建的，就跟着创建
        App13UserExtension.objects.create(user=instance)
    else:
        # 如果是更新的，就跟着更新
        instance.extension.save()


# ----------- 扩展User模型 继承AbstractUser -----------

# 给User模型做扩展，第三种继承 AbstractUser

from django.contrib.auth.models import AbstractUser

'''
使用 给User模型做扩展，第三种继承 AbstractUser，此时User是由我们自定义的，
之前的 create_user 和 create_superuser 已经不适用于创建用户，
因为 objects = UserManager()
因此 要自己定义一个 Manager 类 重写 objects 中的方法属性
'''
from django.contrib.auth.models import BaseUserManager


# 继承 BaseUserManager
class UserManager(BaseUserManager):
    '''
    自定义 UserManager ，改变objects的create_user 和 create_superuser方法
    '''

    # 重写方法
    def _create_user(self, phone, password, **kwargs):

        if not phone:
            raise ValueError('电话不能为空')
        if not password:
            raise ValueError('密码不能为空')

        user = self.model(phone=phone)  # self.model 就指当前的模型对象
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone, password, **kwargs):
        '''  创建普通用户 '''
        kwargs['is_superuser'] = False
        return self._create_user(phone=phone, password=password, **kwargs)

    def create_superuser(self, phone, password, **kwargs):
        '''  创建管理员用户 '''
        kwargs['is_superuser'] = True
        return self._create_user(phone=phone, password=password, **kwargs)


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)  # 如果我们要用phone做登陆验证，那么它必唯一

    # 设置 phone 这个字段为用户登陆验证 时的字段，即 authenticate()方法不再用username做验证，而是phone
    USERNAME_FIELD = 'phone'

    objects = UserManager()


# ----------- 扩展User模型 继承AbstractUser -----------
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin  # PermissionsMixin 涉及到用户权限


# 给User模型做扩展，第三种继承 AbstractBaseUser

class APP13User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    # USERNAME_FIELD 设置验证字段
    USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS 用来在命令行创建超级用户时 提示输入的字段，如果为空 默认为 USERNAME_FIELD 和 password
    REQUIRED_FIELDS = []
    # 自定义objects
    objects = UserManager()

    # 重写 AbstractBaseUser 中的方法
    def get_username(self):
        return self.name


# 以第三种和第四种方式扩展User模型时，如果被外键引用，为了安全 建议使用 get_user_model
from django.contrib.auth import get_user_model


class App13Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    # 使用 get_user_model, 不管以后User模型怎么变它都能找得到正确的关联
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
