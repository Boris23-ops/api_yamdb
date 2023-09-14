from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SignUp, Token

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignUp.as_view(), name='get_token'),
    path('auth/token/', Token.as_view(), name='get_token'),
    path('', include(router_v1.urls)),
]
