from django.urls import path
from rest_framework import routers

from .viewsets import ElementViewSet, CategoryViewSet, TypeViewSet, CommentViewSet

from . import views

route = routers.SimpleRouter()
route.register('element',ElementViewSet)
route.register('category',CategoryViewSet)
route.register('type',TypeViewSet)
route.register('comment',CommentViewSet)

urlpatterns = route.urls

urlpatterns += path('login',views.login),