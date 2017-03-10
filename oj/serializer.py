from django.utils import timezone
from rest_framework import serializers

from .models import *

# 根据当前时区换算时间
class DateTimeFieldWihTZ(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)

class NoticeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', required=False, allow_null=True,
        queryset=User.objects.all()
    )
    date = DateTimeFieldWihTZ(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    class Meta:
        model = Notice
        fields = ('title', 'author', 'date', 'body')
