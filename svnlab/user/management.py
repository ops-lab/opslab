"""
user.management
~~~~~~~~~~~~~~~

This module implements the custom operation of LDAP server.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
"""
import datetime
import json
import jwt
import ldap
import os

from rest_framework.exceptions import APIException


class CustomLdap(object):
    """
    docstring
    """
    # ldap的地址和端口号
    AUTH_LDAP_SERVER_URI = 'ldap://10.1.2.180:389'
    # Authentication: LDAP two
    # root DN
    AUTH_LDAP_BIND_DN = "OU=大华技术,DC=dahuatech,DC=com"
    AUTH_LDAP_BIND_PASSWORD = ""
    AUTH_DOMAIN = "dahuatech"
    # cn, uid, sAMAccountName
    AUTH_LDAP_USER_SEARCH_FILTER_NAME = "sAMAccountName"
    # Retrieve attributes from ldap
    AUTH_LDAP_USER_ATTR_MAP = None
    # AUTH_LDAP_USER_ATTR_MAP = {
    #     'username': 'sAMAccountName',
    #     'email': 'mail',
    #     'telephone': 'telephone',
    #     'truename': 'givenName'
    # }

    def __init__(self, username="", password=""):
        """docstring
        """
        self.server_uri = self.AUTH_LDAP_SERVER_URI
        self.ldap_obj = None
        self.ldap_connect(username, password)

    def ldap_connect(self, username="", password=""):
        """docstring
        """
        url = self.server_uri
        conn = ldap.initialize(url)
        conn.protocol_version = ldap.VERSION3
        if username and not password:
            raise APIException("ERROR: Please input password!")
        try:
            username = '{0}\\{1}'.format(self.AUTH_DOMAIN, username)
            rest = conn.simple_bind_s(username, password)
        except ldap.SERVER_DOWN:
            raise APIException("ERROR: Can't connect to LDAP!")
        except ldap.INVALID_CREDENTIALS:
            raise APIException("ERROR: LADP user failed!")
        except Exception as e:
            raise APIException(type(e))
        # 97 表示success
        if rest[0] != 97:
            raise APIException(rest[1])
        self.ldap_obj = conn

    def ldap_search(self, username=""):
        """
        AUTH_LDAP_BIND_DN: 域
        AUTH_LDAP_USER_SEARCH_FILTER_NAME: 搜索策略
        AUTH_LDAP_USER_ATTR_MAP: 同步账户信息到django的auth_user表中
        username: 搜索的用户
        """
        AUTH_LDAP_USER_SEARCH_FILTER = "({0}={1})".format(
            self.AUTH_LDAP_USER_SEARCH_FILTER_NAME,
            username)
        try:
            search_id = self.ldap_obj.search(self.AUTH_LDAP_BIND_DN,
                                             ldap.SCOPE_SUBTREE,
                                             AUTH_LDAP_USER_SEARCH_FILTER,
                                             self.AUTH_LDAP_USER_ATTR_MAP)
            _, user_data = self.ldap_obj.result(search_id)
            if not user_data:
                return False, []
        except ldap.LDAPError as e:
            raise APIException(e)
        return True, user_data

    def get_user_info(self, username):
        """
        1.获取用户基础信息
        2.解析用户权限，存放至数据库
        """
        user_info = {}
        result, user_infos = self.ldap_search(username)
        truename = user_infos[0][0].split(",")[0].split("=")[1]
        user_info = {
            'username': username,
            'truename': truename,
            'sex': "",
            'email': "",
            'avatar': "",
            'introduction': "",
            'roles': "developer"
        }

        return user_info


def get_token(username):
    """Get user token by username
    iss: JWT签发者
    sub: JWT所面向的用户
    aud: 接收JWT的一方
    exp: JWT的过期时间
    nbf: 定义在什么时间之前，该JWT都是不可用的
    iat: JWT的签发时间
    jti: JWT的唯一身份标识，主要用来作为一次性的token，从而回避重放攻击

    For example:
        >>> token = jwt.encode(
                {
                    'iss': "svnlab",
                    'sub': "svnlab-frontend",
                    'usernmae': "jiuchou",
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
                    'iat': datetime.datetime.utcnow()
                },
                "secret_key,
                algorithm="HS256"
            )
        >>> print(token)
    """
    playload = {
        'iss': "svnlab",
        'sub': "svnlab-frontend",
        'usernmae': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    key = "secret_key"
    token = str(jwt.encode(playload, key, algorithm="HS256"), encoding="utf-8")
    return token


def get_username(token):
    """Verity token: should be True if token is effective value.
    For example:
        >>> jwt.decode(token, "secret_key", algorithm="HS256")
    """
    try:
        decode_token = jwt.decode(token, "secret_key", algorithm="HS256")
        username = decode_token.get("username")
        return username
    except Exception as e:
        return None
