from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notices', views.NoticeViewSet)
router.register(r'users', views.UserViewSet)