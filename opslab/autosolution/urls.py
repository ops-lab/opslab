'''
autosolution.urls
~~~~~~~~~~~~~~~~~

This module implements the Requests Urls.
Requests is an HTTP library, written in Python, for user beings. Basic GET and POST.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.10
'''

from django.urls import path

from autosolution import views as autosolution_views

urlpatterns = [
    path("case", autosolution_views.AutoSolutionView.as_view()),
    path("tools", autosolution_views.trigger_autosolution),
]
