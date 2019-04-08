"""
user.views
~~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for user beings.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
"""
import json
import os

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from rest_framework.views import APIView

from svnlab.svnlab import settings
from svnlab.user.management import CustomLdap, get_token


class UserLoginView(APIView):
    """View of user login operation.
    """

    def post(self, request):
        """User Login by LDAP server
        """
        response = {}
        req = json.loads(request.body.decode())
        username = req['username']
        password = req['password']
        try:
            custom_ldap = CustomLdap(username, password)
            user_info = custom_ldap.get_user_info(username)
            token = get_token(username)
            response['token'] = token
            response['user_info'] = user_info
            response['message'] = "SUCCESS: Login successful!"
            response['status_code'] = 200
            return JsonResponse(response)
        except Exception as e:
            response['message'] = "ERROR: Login failed! {0}".format(e)
            response['status_code'] = 401
            return JsonResponse(response)
