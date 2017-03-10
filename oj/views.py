from django.shortcuts import render
from rest_framework import authentication, permissions, viewsets
from .models import Notice
from .serializer import NoticeSerializer


class DefaultsMiXin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permissions_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.order_by('-date')
    serializer_class = NoticeSerializer