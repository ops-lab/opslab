'''
permission.urls
~~~~~~~~~~~~~~~

This module implements the Requests Urls.
Requests is an HTTP library, written in Python, for user beings. Basic GET and POST.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
'''

from django.urls import path

from permission import views as permission_views

urlpatterns = [
    path("permission-list", permission_views.PermissionView.as_view()),
    path("update-permission", permission_views.update_permission),
]
