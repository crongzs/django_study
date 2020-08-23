from rest_framework import serializers

from app14.models import Merchant, GoodsCategory, Goods

# 序列化的作用
'''
序列化数据ORM >> JSON
验证表单数据 Form
操作数据的增删改查

Serializer 的构造函数需要的参数
instance: 需要传递一个ORM对象或者是一个QuerySet对象，用来将ORM模型序列化为JSON
data: 把需要验证的数据传给data，用来验证这些数据是不是符合要求
many: 如果 instance 传入的对象是一个 QuerySet对象 那么就需要设置为True，否则为False

'''


# --------------- 序列化 ---------------

class MerchantSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True, error_messages={"required": "缺少关键数据name"})
    logo = serializers.CharField(max_length=100, required=True)
    address = serializers.CharField(max_length=200, required=True)
    notice = serializers.CharField(max_length=100, required=False)
    up_send = serializers.DecimalField(required=False, max_digits=6, decimal_places=2)
    lon = serializers.FloatField(required=False)
    lat = serializers.FloatField(required=False)

    def create(self, validated_data):
        return Merchant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''
        :param instance: 模型实例会的对象，数据跟新之前的数据（原来的数据）
        :param validated_data: 是经过验证之后没有问题的数据
        :return:
        '''
        instance.name = validated_data.get('name', instance.name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.address = validated_data.get('address', instance.logo)
        instance.notice = validated_data.get('notice', instance.notice)
        instance.up_send = validated_data.get('up_send', instance.up_send)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.save()
        return instance


# --------------- 模型序列化 ---------------

class MerchantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'
        # exclude = ['name']


# --------------- 嵌套序列化 ---------------


class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    merchant = MerchantModelSerializer(read_only=True)
    merchant_id = serializers.IntegerField(write_only=True)
    goods_list = GoodsModelSerializer(read_only=True, many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'

    def validate_merchant_id(self, value):
        if not Merchant.objects.filter(pk=value).exists():
            raise serializers.ValidationError('商家不存在')
        return value

    def create(self, validated_data):
        merchant_id = validated_data.get('merchant_id')
        merchant = Merchant.objects.get(pk=merchant_id)
        category = GoodsCategory.objects.create(**validated_data, merchant=merchant)
        return category
