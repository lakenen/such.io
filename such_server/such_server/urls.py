from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login$', 'core.views.login_user'),
    url(r'^logout$', 'core.views.logout_user'),
    url(r'^api/', include('api.urls')),
    url(r'^.*$', 'core.views.the_app'),
)
