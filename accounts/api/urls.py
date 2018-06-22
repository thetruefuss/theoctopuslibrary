from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import AuthAPIView, ProfileAPIView, RegisterAPIView

urlpatterns = [
    url(r'^login/$', AuthAPIView.as_view(), name='login'),
    url(r'^register/$', RegisterAPIView.as_view(), name='register'),
    url(r'^settings/$', RegisterAPIView.as_view(), name='settings'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', ProfileAPIView.as_view(), name='profile'),
    url(r'^jwt/$', obtain_jwt_token),
    url(r'^jwt/refresh/$', refresh_jwt_token),
]
