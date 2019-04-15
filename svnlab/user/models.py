"""
user.models
~~~~~~~~~~~

This module implements the Requests Models.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.09
"""
from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    """docstring
    """
    username = models.CharField(max_length=64, unique=True)
    truename = models.CharField(max_length=64)
    sex = models.CharField(verbose_name="sex",
                           max_length=5,
                           choices=(("male", "男"), ("female", "女")),
                           default="male")
    email = models.EmailField()
    introduction = models.CharField(max_length=512)
    avatar_height = models.PositiveIntegerField(default=40, null=True)
    avatar_width = models.PositiveIntegerField(default=40, null=True)
    avatar = models.ImageField(upload_to="avatar",
                               height_field="avatar_height",
                               width_field="avatar_width",
                               null=True)
    roles = models.CharField(max_length=64)
    join_time = models.DateTimeField("加入时间", default=timezone.now)
    login_time = models.DateTimeField("最后登录时间", auto_now=True)

    # [1] https://segmentfault.com/q/1010000006121303
    # python2: def __unicode__
    def __str__(self):
        return self.username

    class Meta:
        """docstring
        """
        managed = True
        db_table = "user_info"
        # 一个字符串的列表或元组, 每个字符串是一个字段名
        #   前面带有可选的"-"前缀表示倒序
        #   前面没有"-"的字段表示正序
        #   使用"?"来表示随机排序
        ordering = ["-username"]
