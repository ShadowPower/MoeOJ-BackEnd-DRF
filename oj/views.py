from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets, filters
from rest_framework.generics import CreateAPIView
from .models import Notice, User
from .serializer import NoticeSerializer, UserSerializer
from .permissions import UserPermission


class DefaultsMiXin(object):
    authentication_classes = [
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = [
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

class NoticeViewSet(DefaultsMiXin, viewsets.ModelViewSet):
    queryset = Notice.objects.order_by('-created_at')
    serializer_class = NoticeSerializer
    search_fields = ('title', 'body')

class UserViewSet(DefaultsMiXin, viewsets.ModelViewSet):
    # 通过用户ID获取对应用户信息
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = get_user_model().objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = ('username', 'email', 'school', 'student_id', 'gender')
    ordering_fields = ('id', 'username', 'email', 'student_id', 'created_at')
    permission_classes = [UserPermission]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        return super(UserViewSet, self).get_permissions()