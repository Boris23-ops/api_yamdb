from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import Token, SignUp, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')


auth_urls = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', Token.as_view(), name='token')
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router_v1.urls)),
]
