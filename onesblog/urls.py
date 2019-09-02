
from django.urls import re_path
from onesblog import views

urlpatterns = [
    re_path('(?P<surfix>\w+)/(?P<type>\w+)/(?P<type_id>\d+)/$',views.onesindex,name='onesindex_filter'),
    re_path('(?P<surfix>\w+)/PostAvatar/$', views.PostAvatar, name='PostAvatar'),
    re_path('(?P<surfix>\w+)/ChangeAvatar/$', views.ChangeAvatar, name='ChangeAvatar'),
    re_path('(?P<surfix>\w+)/$', views.onesindex,name='onesindex'),

    # re_path('(?P<article_type_id>\d+)/$', views.onesindex,name='onesindex'),
]
