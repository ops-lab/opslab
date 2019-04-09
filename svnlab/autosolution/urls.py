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

from svnlab.autosolution import views as autosolution_views

urlpatterns = [
    path("update-caselib", autosolution_views.update_caselib),
]
