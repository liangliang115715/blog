"""blog2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from screen import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('login/', views.login, name='login'),
    path('regist/', views.regist, name='regist'),
    re_path('regBlog/(?P<user>.+)/$', views.regBlog, name='regBlog'),
    path('logout/', views.logout, name='logout'),
    re_path('index', include('onesblog.urls')),
    re_path('articals/(?P<artical_id>\d+)/$', views.artical_detail, name='artical_detail'),
    re_path('articals/ckediter/uploadimg/$', views.ckediter_uploadimg, name='ckediter_uploadimg'),
    re_path('(?P<article_type_id>\d+)/$', views.index,name='home'),

]
