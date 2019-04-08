"""
user.models
~~~~~~~~~~~

This module implements the Requests Models.

:copyright: (c) 2019 by jiuchou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.15
"""
from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    """
        state: {
            token: getToken(),
            avatar: "",
            userInfo: {
                username: "guster",
                truename: "",
                sex: "male",
                email: "xxx@dahuatech.com",
                introduction: "",
                avatar: ""
            }
        }
    """
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    truename = models.CharField(max_length=64)
    sex = models.CharField(verbose_name="sex",
                           max_length=5,
                           choices=(("male", "male"), ("female", "female")),
                           default="male")
    email = models.EmailField()
    telephone = models.CharField(max_length=64, unique=True)
    introduction = models.CharField(max_length=512)
    profile_photos_height = models.PositiveIntegerField(default=75)
    profile_photos_width = models.PositiveIntegerField(default=75)
    profile_photos = models.ImageField(upload_to="profile_photos",
                                       height_field="profile_photos_height",
                                       width_field="profile_photos_width")
    join_time = models.DateTimeField("加入时间", default=timezone.now)
    login_time = models.DateTimeField("最后登录时间", auto_now=True)

    # [1] https://segmentfault.com/q/1010000006121303
    # python2: def __unicode__
    def __str__(self):
        return self.username
