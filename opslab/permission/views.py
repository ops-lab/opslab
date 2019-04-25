"""
permission.views
~~~~~~~~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for permission beings.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
"""
import json
import os
import time

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from permission.models import (PermissionDeveloper, PermissionOwner,
                               PermissionReport)
from opslab import settings
from user.management import get_username


class PermissionView(APIView):
    """View of permission.
    """

    def _get_permissions(self, role):
        try:
            # role: developer, owner, admin
            if role == "developer":
                permissions = PermissionDeveloper.objects.filter(username=username)\
                    .exclude(permission=0)\
                    .values("username",
                            "module",
                            "path",
                            "url",
                            "owner",
                            "permission").order_by("url")
            elif role == "owner":
                permissions = PermissionOwner.objects.filter(owner=username)\
                    .values("owner",
                            "module",
                            "path",
                            "url",
                            "reader",
                            "writer",
                            "reader_number",
                            "writer_number").order_by("url")
            elif role == "admin":
                pass
            else:
                permissions = None
        except Exception as e:
            raise APIException("ERROR: Get permissions from database failed!")
        return permissions

    def _get_permission_list(self, role, limit, page):
        permission_list = []
        total = 0

        permissions = _get_permissions(role)
        total = len(permissions)

        paginator = Paginator(permissions, limit)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of resluts.
            contacts = paginator.page(paginator.num_pages)

        for permission in contacts:
            permission_list.append(permission)

        return permission_list, total

    def get(self, request):
        """User get permission list.

        User get permission list information by role(developer/owner/admin)
        from database.
        """
        response = {}
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            username = get_username(token)
        except Exception as e:
            response['message'] = "ERROR: Verify authentication failed! {0}".format(
                e)
            response['status_code'] = 401
            return JsonResponse(response)

        req = request.GET
        limit = req['limit']
        page = req['page']
        role = req['role']
        try:
            permission_list, total = _get_permission_list(role, limit, page)
        except Exception as e:
            response['message'] = "ERROR: Get permission list information failed!"
            response['status_code'] = 500
            return JsonResponse(response)

        response['permission_list'] = permission_list
        response['message'] = "SUCCESS: Get permission list information successful!"
        response['status_code'] = 200
        return JsonResponse(response)

    def _update_permission_by_developer(self, username, role):
        cmd = "bash {0}/common/utils/getPermissionDeveloper.sh {1}".format(
            settings.BASE_DIR,
            username)
        result = os.system(cmd)
        if result == 0:
            message = "SUCCESS: Update PermissionDeveloper table by \
                        {0} successful!".format(username)
        else:
            message = "ERROR: Update PermissionDeveloper table by \
                        {0} failed!".format(username)
            raise APIException(message)

    def _get_subpaths(self, module, path):
        subpaths = []

        # filename = "authfilename"
        filename = "{0}/common/statics/dav_svn.authz".format(settings.BASE_DIR)
        with open(filename, 'r') as f:
            text = f.read()
        # import re
        # text = open('zz','r').read()
        # regex = r"[{0}:/{1}.*".format(module,path)
        path_infos = re.findall(regex, text)
        for path_info in path_infos:
            subpath = path_info.strip('/').strip('[')
            subpaths.append(subpath)

        return subpaths

    def _get_url(self, module, path):
        """Get url.

        Get url by module and path.
        """
        url = ""

        # filename = "module_preurl_map"
        filename = "{0}/common/statics/module_preurl_map".format(
            settings.BASE_DIR)
        with open(filename, 'r') as f:
            text = f.read()
        regex = "{0}(.*)".format(module)
        preurl = re.findall(regex, text)[0].strip(',').strip('/')
        url = "{0}/{1}/{2}".format(preurl, module, path)

        return url

    def _get_owner(self, url):
        """Get owner.

        Get owner by url from owner_url_map
        """
        owner = ""

        # filename = "owner_url_map"
        filename = "{0}/common/statics/owner_url_map".format(settings.BASE_DIR)
        with open(filename, 'r') as f:
            text = f.read()
        regex = "(.*){0}\n".format(url)
        owner = re.findall(regex, text)[0].strip(',')

        return owner

    def _get_reader_and_writer(self, module, path):
        """Get reader and writer.

        Get reader and writer by module and path.
        """
        reader = ""
        writer = ""

        # filename = "authfilename"
        filename = "{0}/common/statics/dav_svn.authz".format(settings.BASE_DIR)
        with open(filename, 'r') as f:
            text = f.read()
            # import re
            # text=open("zz','r').read()
            # regex = r"[Documents:/IVSDocs/智能算法部/TDT/技术预研项目/DH3.RD002064_基础算法部预研]
            regex = r"[{0}:/{1}]".format(module, path)
            permission_list = text.split(regex)[1].split('[')[
                0].strip().split('\n')
            for permission in permission_list:
                if "=rw" in permission:
                    reader = reader + permission.split("=")[0]
                else:
                    writer = writer + permission.split("=")[0]

        resder = reader.strip(",")
        writer = writer.strip(",")

        return reader, writer

    def _update_permission_by_owner(self, module, path):
        try:
            url = _get_url(module, path)
            owner = _get_owner(url)
            reader, writer = _get_reader_and_writer(module, path)

            permission_info = {
                'module': module,
                'path': path,
                'url': url,
                'owner': owner,
                'reader': reader,
                'writer': writer,
                'reader_number': reader_number,
                'writer_number': writer_number,
            }
            PermissionOwner.objects.update_or_create(
                url=url, defaults=permission_info)
        except Exception as e:
            raise APIException(
                "ERROR: Update or create permission information failed.")

    def post(self, request):
        """User get permission list.

        User get permission list information to database by role
        (developer/owner/admin) from authfile.
        """
        response = {}
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            username = get_username(token)
        except Exception as e:
            response['message'] = "ERROR: Verify authentication failed! {0}".format(
                e)
            response['status_code'] = 401
            return JsonResponse(response)

        req = json.loads(request.body.decode())
        role = req['role']
        try:
            # role: developer, owner, admin
            if role == "developer":
                _update_permission_by_developer(username, role)
            elif role == "owner":
                module = req['module']
                path = req['path']

                subpaths = _get_subpaths(module, path)
                for subpath in subpaths:
                    _update_permission_by_owner(module, subpath)
            elif role == "admin":
                pass
            else:
                pass
        except Exception as e:
            response['message'] = "ERROR: Update permission list information to database failed!"
            response['status_code'] = 500
            return JsonResponse(response)

        response['message'] = "SUCCESS: Update permission list information to database successful!"
        response['status_code'] = 200
        return JsonResponse(response)


def update_permission(request):
    """Update permission.

    Update permission by detail information.
    """
    response = {}
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    identifier = 'opslab{}'.format(timestamp)
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        applicant = get_username(token)
    except Exception as e:
        response['message'] = "ERROR: Verify authentication failed! {0}".format(
            e)
        response['status_code'] = 401
        return JsonResponse(response)

    req = json.loads(request.body.decode())
    print(req)
    path = req['path']
    module = req['module']
    username = req['username']
    old_permission = req['old_permission']
    new_permission = req['new_permission']
    try:
        if PermissionReport.objects.filter(username=username,
                                           path=path,
                                           module=module,
                                           status=0):
            print("WARNING: username({0}) is running".format(username))
        else:
            PermissionReport.objects.create(identifier=identifier,
                                            path=path,
                                            module=module,
                                            username=username,
                                            applicant=applicant,
                                            old_permission=old_permission,
                                            new_permission=new_permission,
                                            status=0)
    except Exception:
        response['message'] = "ERROR: Update status for PermissionReport failed!"
        response['status_code'] = 500
        return JsonResponse(response)

    # Update permission
    authfile = "{0}/common/statics/dav_svn.authz".format(settings.BASE_DIR)
    cmd = "bash {0}/common/utils/update_authfile.sh {1} {2} {3} {4} {5}".format(
        BASE_DIR,
        authfile,
        module,
        path,
        username,
        new_permission
    )
    print(cmd)
    result = os.system(cmd)

    # Update database
    try:
        if result == 0:
            PermissionReport.objects.filter(
                username=username,
                module=module,
                path=path,
                status=0).update(status=1)
            # developer
            PermissionDeveloper.objects.filter(
                username=username,
                module=module,
                path=path).update(permission=new_permission)
            # owner
            # 获取模块数据库表中对应的人员名单，删除
        else:
            PermissionReport.objects.filter(username=username,
                                            path=path,
                                            module=module,
                                            status=0).update(status=2)
    except Exception:
        response['message'] = "ERROR: Write database PermissionReport status failed!"
        response['status_code'] = 500
        return JsonResponse(response)

    response['message'] = "SUCCESS: Update permission information successful!"
    response['status_code'] = 200
    return JsonResponse(response)
