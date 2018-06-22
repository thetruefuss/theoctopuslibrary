from django.conf.urls import url

from .views import (MessageCreateAPIView, ReplyCreateAPIView,
                    ThreadListAPIView, ThreadRetrieveAPIView)

urlpatterns = [
    url(r'^inbox/$', ThreadListAPIView.as_view(), name='thread_list'),
    url(r'^create/$', MessageCreateAPIView.as_view(), name='message_create'),
    url(r'^reply/$', ReplyCreateAPIView.as_view(), name='reply_create'),
    url(r'^thread/(?P<pk>\d+)/$', ThreadRetrieveAPIView.as_view(), name='thread_retrieve'),
]
