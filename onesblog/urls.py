
from django.contrib import admin
from django.urls import path,re_path,include
from onesblog import views

urlpatterns = [
    re_path('(?P<surfix>\w+)/(?P<type>\w+)/(?P<type_id>\d+)/$',views.onesindex,name='onesindex'),
    re_path('(?P<surfix>\w+)/$', views.onesindex,name='onesindex'),

    # re_path('(?P<article_type_id>\d+)/$', views.onesindex,name='onesindex'),
]
