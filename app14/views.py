from app14.models import Merchant, GoodsCategory, Goods

from app14.serializers import MerchantSerializer, MerchantModelSerializer, GoodsCategoryModelSerializer, \
    GoodsModelSerializer

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def merchant1(request):
    if request.method == 'GET':
        queryset = Merchant.objects.all()
        serializer = MerchantSerializer(instance=queryset, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    else:
        serializer = MerchantSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)  # serializer.data 经过序列化后的数据
        else:
            return JsonResponse(serializer.errors, status=400)


def merchant2(request):
    if request.method == 'GET':
        queryset = Merchant.objects.all()
        serializer = MerchantModelSerializer(instance=queryset, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    else:
        serializer = MerchantModelSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)  # serializer.data 经过序列化后的数据
        else:
            return JsonResponse(serializer.errors, status=400)


def goods1(request):
    if request.method == 'GET':
        queryset = Goods.objects.all()
        serializers = GoodsModelSerializer(instance=queryset, many=True)
        return JsonResponse(serializers.data, status=200, safe=False)
    else:
        serializer = GoodsModelSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)


# --------------- 嵌套序列化 ---------------

def category1(request):
    if request.method == 'GET':
        queryset = GoodsCategory.objects.all()
        serializers = GoodsCategoryModelSerializer(instance=queryset, many=True)
        return JsonResponse(serializers.data, status=200, safe=False)
    else:
        serializer = GoodsCategoryModelSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)


# --------------- 类视图 ---------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class MerchantAPIView(APIView):
    """
    检索, 更新和删除一个merchant实例对象.
    """

    def get_object(self, pk):
        try:
            return Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            merchant = self.get_object(pk)
            serializer = MerchantModelSerializer(merchant)
            return Response(serializer.data)
        else:
            queryset = Merchant.objects.all()
            serializer = MerchantModelSerializer(instance=queryset, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        merchant = self.get_object(pk)
        serializer = MerchantModelSerializer(merchant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        merchant = self.get_object(pk)
        merchant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------- Mixins ---------------
from rest_framework import generics
from rest_framework import mixins


class MerchantView1(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):
    queryset = Merchant
    serializer_class = MerchantModelSerializer

    def get(self, request, pk=None):
        if pk:
            # 如果url带了pk，那么就返回单个详情
            return self.retrieve(request)
        else:
            # 没有带pk，就返回列表
            return self.list(request)

    # 如果要更改添加的逻辑，应该去重写 perform_create 方法
    def perform_create(self, serializer):
        serializer.save(created=self.request.user)

    def post(self, request):
        # 如果要更改添加的逻辑，应该去重写 perform_create 方法
        return self.create(request)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# --------------- Generic类视图 ---------------

class MerchantView2(
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView):
    queryset = Merchant
    serializer_class = MerchantModelSerializer


# --------------- 视图集 ---------------


from rest_framework import viewsets
from rest_framework.decorators import action


class MerchantModelViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantModelSerializer

    # 自定义action 实现自己单独的路由，比如商家里面保函 之 字的

    @action(['GET'], detail=False)  # 第一个参数为请求方式 第二个参数 detail表示url是不是需要带id查询，需要True不需要False
    def the(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = queryset.filter(name__contains='之')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(result, many=True)
        return Response(serializer.data)


# --------------- 认证 ---------------
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class MerchantModelViewSet01(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantModelSerializer

    # authentication_classes 用来验证用户是否成功登陆
    authentication_classes = [BasicAuthentication, ]  # 是 BasicAuthentication 不是 BaseAuthentication
    # permission_classes 根据用户的权限限制访问
    permission_classes = [IsAuthenticated, ]  # IsAuthenticated 登陆之后才能访问

    # HEADER_ENCODING
    # basic username:password >经过> base64.b64encode(b'')


# --------------- JWT(JSON Web Token)认证 ---------------

'''
模拟 JWT(JSON Web Token)认证 登陆
'''
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view

from app14.authentications import gengerate_jwt, JWTTokenAuthentication

User = get_user_model()


@api_view(['GET'])  # 使用这个装饰器，将视图函数变成一个api view
def token_view(request):
    ''' 模拟用户登陆，添加token '''
    user = User.objects.first()
    token = gengerate_jwt(user)
    return Response({'token': token}, status=status.HTTP_200_OK)


class MerchantModelViewSet02(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantModelSerializer

    # authentication_classes 用来验证用户是否成功登陆
    authentication_classes = [JWTTokenAuthentication, BasicAuthentication]
    # permission_classes 根据用户的权限限制访问
    permission_classes = [IsAuthenticated, ]


# --------------- 权限 ---------------
from app14.permissions import MyPermission


class MerchantModelViewSet03(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantModelSerializer

    authentication_classes = [JWTTokenAuthentication, BasicAuthentication]
    permission_classes = [MyPermission, IsAuthenticated]


# --------------- 限速截流 ---------------
class MerchantModelViewSet04(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantModelSerializer
