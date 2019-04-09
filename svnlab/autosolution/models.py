"""
autosolution.models
~~~~~~~~~~~~~~~~~~~

This module implements the Requests Models.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.10
"""
from django.db import models


class CaseLib(models.Model):
    """知识库：用于自助解决方案工具
    """
    id = models.IntegerField(blank=True, null=True)
    case_key = models.CharField(max_length=512, blank=True, null=True)
    case_info = models.CharField(max_length=512, blank=True, null=True)
    case_type = models.CharField(max_length=512, blank=True, null=True)
    case_description = models.CharField(max_length=512, blank=True, null=True)
    case_solution = models.CharField(max_length=512, blank=True, null=True)
    case_remark = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        """CaseLib meta data
        """
        managed = True
        db_table = "case_lib"
        db_table = "auto_solution"
