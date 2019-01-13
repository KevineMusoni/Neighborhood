from django.conf.urls import url,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^edit/profile/$',views.edit_profile,name='edit_profile'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^hoods/new/post/(\d+)$', views.new_post, name='new-post'),
    url(r'^hoods/new/comment/(\d+)',views.newcomment, name='newcomment'),
    url(r'^location$', views.location, name='location'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^hoods/new/business/(\d+)$',views.post_business, name='new-business'),
    url(r'^hoods/(\d+)',views.hoods,name='hoods'),
    url(r'^new/hood$', views.new_hood, name='new-hood')

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)