from django.db import models


class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    is_delete = models.BooleanField(default=False, verbose_name="删除标记")

    class Meta:

        abstract = True  # 只作为基类,不创建数据表
