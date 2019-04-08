'''
user.urls
~~~~~~~~~

This module implements the Requests Urls.
Requests is an HTTP library, written in Python, for user beings. Basic GET and POST.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
'''

from django.urls import path

from svnlab.user import views as user_views

urlpatterns = [
    path('login', user_views.UserLoginView.as_view()),
]
