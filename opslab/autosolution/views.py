"""
autosolution.views
~~~~~~~~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for autosolution beings.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.10
"""
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from autosolution.jenkins_api import trigger_job
from autosolution.models import CaseLib


class AutoSolutionView(APIView):
    """View of auto-solution.
    """

    def post(self, request):
        """docstring
        """
        response = {}

        req = json.loads(request.body.decode())
        print(req)
        try:
            for case_list in req:
                print(case_list)
                case_info = {
                    'case_key': case_list.get('case_key'),
                    'case_info': case_list.get('case_info'),
                    'case_info': case_list.get('case_info'),
                    'case_type': case_list.get('case_type'),
                    'case_description': case_list.get('case_description'),
                    'case_solution': case_list.get('case_solution'),
                    'case_remark': case_list.get('case_remark')
                }
                CaseLib.objects.update_or_create(
                    case_key=case_list.get('case_key'),
                    case_info=case_list.get('case_info'),
                    case_type=case_list.get('case_type'),
                    case_description=case_list.get('case_description'),
                    case_solution=case_list.get('case_solution'),
                    case_remark=case_list.get('case_remark'),
                    defaults=case_info)
        except Exception as e:
            response['message'] = "ERROR: Update caselib information to database failed!"
            response['status_code'] = 500
            return JsonResponse(response)

        response['message'] = "SUCCESS: Update caselib information to database successful!"
        response['status_code'] = 200
        return JsonResponse(response)


    def _get_case_list(self, limit, page):
        case_list = []
        cases = []

        try:
            # cases = _get_cases()
            cases = CaseLib.objects.values().order_by('case_key')
        except Exception as e:
            raise APIException("ERROR: Get cases from database failed! {0}".format(e))
        total = len(cases)

        paginator = Paginator(cases, limit)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of resluts.
            contacts = paginator.page(paginator.num_pages)

        for case in contacts:
            case_list.append(case)

        return case_list, total

    def get(self, request):
        """Get auto-solution case list information.

        Get auto-solution case list information from database.
        """
        response = {}

        request.encoding = 'utf-8'
        req = request.GET
        limit = req['limit']
        page = req['page']
        try:
            case_list, total = self._get_case_list(limit, page)
        except Exception as e:
            message = "ERROR: Get case list information failed! {0}".format(e)
            response['message'] = message
            response['status_code'] = 500
            return JsonResponse(response)

        response['case_list'] = case_list
        response['total'] = total
        response['message'] = "SUCCESS: Get case list information successful!"
        response['status_code'] = 200
        return JsonResponse(response)

def trigger_autosolution(request):
    """docString
    """
    response = {}

    req = json.loads(request.body.decode())
    print(req)
    try:
        build_url = req.get('build_url')
        receivers = req.get('receivers')
        stage = req.get('stage')
        mode = req.get('mode')
        print(build_url)
        print(receivers)
        trigger_job(build_url, receivers, stage, mode)
    except Exception as e:
        response['message'] = "ERROR: Trigger autosolution failed! {0}".format(e)
        response['status_code'] = 500
        return JsonResponse(response)

    response['message'] = "SUCCESS: Trigger autosolution successful!"
    response['status_code'] = 200
    return JsonResponse(response)
    
