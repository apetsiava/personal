from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^bar/create/$', login_required(BarCreateView.as_view()), name='bar_create'),
    url(r'bar/$', login_required(BarListView.as_view()), name='bar_list'),
    url(r'^bar/(?P<pk>\d+)/$', login_required(BarDetailView.as_view()), name='bar_detail'),
    url(r'^bar/update/(?P<pk>\d+)/$', login_required(BarUpdateView.as_view()), name='bar_update'),
    url(r'^bar/delete/(?P<pk>\d+)/$', login_required(BarDeleteView.as_view()), name='bar_delete'),
    url(r'^bar/(?P<pk>\d+)/comment/create/$', login_required(CommentCreateView.as_view()), name='comment_create'),
    url(r'^bar/(?P<bar_pk>\d+)/comment/update/(?P<comment_pk>\d+)/$', login_required(CommentUpdateView.as_view()), name='comment_update'),
    url(r'^bar/(?P<bar_pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', login_required(CommentDeleteView.as_view()), name='comment_delete'),
    url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
)