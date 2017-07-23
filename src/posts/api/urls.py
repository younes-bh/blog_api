from django.conf.urls import url, include
from django.contrib import admin


from .views import (
    PostListAPIView
    )


urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
]
