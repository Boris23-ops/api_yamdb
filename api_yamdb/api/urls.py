from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genre', GenreViewSet)
router.register('title', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
