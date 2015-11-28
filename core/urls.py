from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^bar/create/$', BarCreateView.as_view(), name='bar_create'),
    url(r'bar/$', BarListView.as_view(), name='bar_list'),
    url(r'^bar/(?P<pk>\d+)/$', BarDetailView.as_view(), name='bar_detail'),
    url(r'^bar/update/(?P<pk>\d+)/$', BarUpdateView.as_view(), name='bar_update'),
    url(r'^bar/delete/(?P<pk>\d+)/$', BarDeleteView.as_view(), name='bar_delete'),
    url(r'^bar/(?P<pk>\d+)/comment/create/$', CommentCreateView.as_view(), name='comment_create'),
    url(r'^bar/(?P<bar_pk>\d+)/comment/update/(?P<comment_pk>\d+)/$', CommentUpdateView.as_view(), name='comment_update'),
    url(r'^bar/(?P<bar_pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', CommentDeleteView.as_view(), name='comment_delete'),
)