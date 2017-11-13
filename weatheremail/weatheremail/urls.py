from django.conf.urls import include, url
from django.contrib import admin
import signupform.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'weatheremail.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include(signupform.urls)),
	url(r'^subscribe/', include(signupform.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
