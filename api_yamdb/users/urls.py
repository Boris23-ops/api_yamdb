from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import Token, SignUp, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignUp.as_view()),
    path('auth/token/', Token.as_view()),
    path('', include(router.urls)),
]
