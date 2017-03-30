from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include, url

import api_0_1

app_name='share'
urlpatterns = [
	url(r'^api/0_1/current-user$', api_0_1.AuthView_0_1.as_view(), name='current_user_api_0_1'),
]
