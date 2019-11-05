from django.db import models
from user.models import User
from db.base_model import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=30)

    def __str__(self):

        return self.tag_name


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


# class RichTextUploadingField(object):
#     pass


class Content(BaseModel):
    '''文章表'''

    status_choices = (
        (0, "上线"),
        (1, "下线")
    )

    title = models.CharField(max_length=70, verbose_name="文章标题")
    slug = models.CharField(max_length=200, blank=True, null=True, verbose_name="文章概述")
    text = RichTextUploadingField()
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name="文章状态")
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name="分类")
    tags = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, verbose_name="标签")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content"
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["-created"]

    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])

class Comment(BaseModel):

    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False, verbose_name="回复内容")
    article = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="所属文章")
    reply = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="回复")

    class Meta:
        db_table = "comment"
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text