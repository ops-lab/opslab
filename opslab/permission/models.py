"""
permission.models
~~~~~~~~~~~~~~~~~

This module implements the Requests Models.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
"""
from django.db import models
from django.utils import timezone


class PermissionDeveloper(models.Model):
    """docstring
    """
    username = models.CharField(max_length=50, blank=True, null=True)
    module = models.CharField(max_length=50, blank=True, null=True)
    path = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    owner = models.CharField(max_length=50, blank=True, null=True)
    permission = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        """docstring
        """
        managed = True
        db_table = "permission_developer"


class PermissionOwner(models.Model):
    """docstring
    """
    module = models.CharField(max_length=64, blank=True, null=True)
    path = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)
    owner = models.CharField(max_length=64, blank=True, null=True)
    reader = models.CharField(max_length=512, blank=True, null=True)
    writer = models.CharField(max_length=512, blank=True, null=True)
    reader_number = models.IntegerField(blank=True)
    writer_number = models.IntegerField(blank=True)

    class Meta:
        """docstring
        """
        managed = True
        db_table = "permission_owner"


class PermissionReport(models.Model):
    """定义svn操作记录
    包含
        影响人
        申请人
        旧权限
        新权限
        操作状态
        申请来源
        申请时间
        最后更新时间
    """
    STATUS_CHOICES = ((0, '进行中'), (1, '成功'), (2, '失败'))
    identifier = models.CharField(max_length=64, unique=True)
    path = models.CharField(max_length=512)
    module = models.CharField(max_length=512)
    username = models.CharField(max_length=64)
    applicant = models.CharField(max_length=64)
    old_role = models.CharField(max_length=64)
    new_role = models.CharField(max_length=643)
    status = models.IntegerField(choices=STATUS_CHOICES)
    apply_time = models.DateTimeField('申请时间', default=timezone.now)
    update_time = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        """Roport meta data.
        """
        managed = True
        db_table = 'permission_report'
