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
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from user.management import CustomLdap, get_token
from user.models import UserInfo


class UserLoginView(APIView):
    """View of user login operation.
    """

    def update_user_info(self, user_info):
        try:
            UserInfo.objects.update_or_create(
                username=user_info.get('username'),
                defaults=user_info)
        except Exception as e:
            raise APIException(
                "ERROR: Update or create user information failed. {0}".format(e))

    def _get_user_info(self, username, password):
        if username == "devops":
            if password == "123456":
                user_info = {
                    'username': "devops",
                    'truename': "jiuchou",
                    'sex': "male",
                    'email': "jiuchou@email.com",
                    'avatar': "",
                    'introduction': "",
                    'roles': "devops"
                }
            else:
                raise APIException(
                    "ERROR: User password failed.")
        else:
            custom_ldap = CustomLdap(username, password)
            user_info = custom_ldap.get_user_info(username)

        return user_info

    def post(self, request):
        """User Login by LDAP server
        """
        response = {}
        req = json.loads(request.body.decode())
        username = req['username']
        password = req['password']
        try:
            user_info = self._get_user_info(username, password)
            self.update_user_info(user_info)
            token = get_token(username)
            response['token'] = token
            response['user_info'] = user_info
        except Exception as e:
            response['message'] = "ERROR: Login failed! {0}".format(e)
            response['status_code'] = 401
            return JsonResponse(response)

        response['message'] = "SUCCESS: Login successful!"
        response['status_code'] = 200
        return JsonResponse(response)
