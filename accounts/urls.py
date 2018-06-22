from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/accounts/settings/')),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^settings/$', accounts_views.settings, name='settings'),
    url(r'^deactivated_threads/$', accounts_views.deactivated_book_threads, name='deactivated_book_threads'),

    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^account_activation_sent/$', accounts_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        accounts_views.activate, name='activate'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^ajax/validate_username/$', accounts_views.validate_username, name='validate_username'),

    url(r'^(?P<username>[\w.@+-]+)/$', accounts_views.book_threads, name='book_threads'),
    url(r'^(?P<username>[\w.@+-]+)/profile/$', accounts_views.user_profile, name='user_profile'),
]
