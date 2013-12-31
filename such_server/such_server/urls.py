from django.conf.urls import patterns, include, url
from django.contrib import admin

from realtime.views import BroadcastChatView

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^chat', BroadcastChatView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'core.views.login_user'),
    url(r'^.*$', 'core.views.the_app'),
)
