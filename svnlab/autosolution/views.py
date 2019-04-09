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

from django.http import JsonResponse

from svnlab.autosolution.models import CaseLib


def update_caselib(request):
    """docstring
    """
    response = {}

    req = json.loads(request.body.decode())
    print(req)
    try:
        for case_list in req:
            print(case_list)
            CaseLib.objects.create(
                case_key=case_list.get('case_key'),
                case_info=case_list.get('case_info'),
                case_type=case_list.get('case_type'),
                case_description=case_list.get('case_description'),
                case_solution=case_list.get('case_solution'),
                case_remark=case_list.get('case_remark'))
    except Exception as e:
        response['message'] = "ERROR: Update caselib information to database failed!"
        response['status_code'] = 500
        return JsonResponse(response)

    response['message] = "SUCCESS: Update caselib information to database successful!"
    response['status_code'] = 200
    return JsonResponse(response)
