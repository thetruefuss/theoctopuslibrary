from django.conf.urls import url

from .views import (BookCreateAPIView, BookDestroyAPIView, BookListAPIView,
                    BookRetrieveAPIView, BookUpdateAPIView)

urlpatterns = [
    url(r'^$', BookListAPIView.as_view(), name='books_list'),
    url(r'^create/$', BookCreateAPIView.as_view(), name='books_create'),
    url(r'^(?P<slug>[\w-]+)/$', BookRetrieveAPIView.as_view(), name='books_retrieve'),
    url(r'^(?P<slug>[-\w]+)/edit/$', BookUpdateAPIView.as_view(), name='books_update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', BookDestroyAPIView.as_view(), name='books_delete'),
]
