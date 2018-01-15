"""app URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<postid>[^/]+)$', views.post, name='post'),
    url(r'^flag1$', views.flag1, name='flag1'),
    url(r'^flag2$', views.flag2, name='flag2'),
    url(r'^flag_api$', views.flag_api, name='flag_api'),
    url(r'^publish$', views.publish, name='publish'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^login/$', auth_views.login,
            dict(template_name='blog/login.html'), name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    # url(r'^admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
