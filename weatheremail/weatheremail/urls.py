from django.conf.urls import include, url
from django.contrib import admin
import signupform.urls

urlpatterns = [
    #this is to make the root url work to default subscribe
    url(r'^$', include(signupform.urls)),
	url(r'^subscribe/', include(signupform.urls)),
    #admin url
    url(r'^admin/', include(admin.site.urls)),
]
