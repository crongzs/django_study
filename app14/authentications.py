import jwt
import time
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

User = get_user_model()


def gengerate_jwt(user):
    """
    生成 JWT token
    :param user:
    :return:
    """
    timestamp = int(time.time()) + 60 * 60 * 6  # 6 个小时过期

    result = jwt.encode({'userid': user.pk, 'exp': timestamp}, settings.SECRET_KEY)
    # 将 bytes类型的result用decode解码成str类型
    return result.decode('utf-8')


class JWTTokenAuthentication(BaseAuthentication):
    """
        Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'JWT'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Authorization 不可用'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Authorization 不可用 缺少空格'
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            # jwt解码
            jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY)
            userid = jwt_info.get('userid')
            try:
                user = User.objects.get(pk=userid)
                return (user, jwt_token)
            except:
                msg = '用户不存在'
                raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignatureError:
            msg = '过期失效的令牌'
            raise exceptions.AuthenticationFailed(msg)
