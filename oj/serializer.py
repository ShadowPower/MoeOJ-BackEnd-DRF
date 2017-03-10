from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, status
from rest_framework.exceptions import *
from rest_framework.response import Response

from .models import *

class DateTimeFieldWihTZ(serializers.DateTimeField):
    """根据当前时区换算时间"""
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)

class NoticeSerializer(serializers.ModelSerializer):
    """序列化公告内容"""
    # 根据作者的用户ID查询用户名
    author = serializers.SlugRelatedField(
        slug_field='username', required=False, allow_null=True,
        queryset=User.objects.all()
    )
    # 根据时区设置，格式化时间文本，创建公告时不需要指定时间
    date = DateTimeFieldWihTZ(source='created_at', format="%Y-%m-%d %H:%M", required=False, read_only=True)
    class Meta:
        model = Notice
        fields = ('title', 'author', 'date', 'body')

class UserSerializer(serializers.ModelSerializer):
    """序列化用户信息"""
    email = serializers.CharField()
    created_at = DateTimeFieldWihTZ(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                school=validated_data['school'],
                student_id=validated_data['student_id'],
                gender=validated_data['gender'],
            )
            if 'password' in validated_data:
                user.set_password(validated_data['password'])
                user.save()
            else:
                raise NotAcceptable(detail={'err':'您还没有输入密码'})
        except:
            raise NotAcceptable(detail={'err': '注册失败，也许是用户已经存在了'})
        return user

    def update(self, instance, validated_data):
        user = authenticate(email=validated_data['email'], password=validated_data['password'])
        if user is not None:
            instance.username=validated_data['username']
            instance.email=validated_data['email']
            instance.school=validated_data['school']
            instance.student_id=validated_data['student_id']
            instance.gender=validated_data['gender']
            instance.save()
        else:
            raise ValidationError(detail={'err':'要想更改信息，请输入正确的密码'})
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'school', 'student_id', 'gender', 'created_at', 'password')