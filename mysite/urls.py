"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from books import views as books_views
from core import views as core_views

urlpatterns = [
    url(r'^$', books_views.homepage, name='homepage'),
    url(r'^results/$', books_views.search_results, name='search_results'),
    url(r'^book/(?P<book_slug>[-\w]+)/$', books_views.book_detail, name='book_detail'),
    url(r'^submit/$', books_views.book_post, name='book_post'),
    url(r'^ajax/contact_details/(?P<book_id>\d+)/$', books_views.contact_details, name='contact_details'),
    url(r'^ajax/deactivate_book/(?P<book_id>\d+)/$', books_views.deactivate_book, name='deactivate_book'),
    url(r'^ajax/activate_book/(?P<book_id>\d+)/$', books_views.activate_book, name='activate_book'),

    url(r'^report/$', core_views.report, name='report'),
    url(r'^feedback/$', core_views.feedback, name='feedback'),
    url(r'^terms/$', core_views.terms, name='terms'),
    url(r'^privacy/$', core_views.privacy, name='privacy'),
    url(r'^about/$', core_views.about, name='about'),
    url(r'^faq/$', core_views.faq, name='faq'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^messages/', include('pinax.messages.urls', namespace='pinax_messages')),

    url(r'^api/accounts/', include('accounts.api.urls', namespace='accounts-api')),
    url(r'^api/books/', include('books.api.urls', namespace='books-api')),
    url(r'^api/messages/', include('pinax.messages.api.urls', namespace='messages-api')),


    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
