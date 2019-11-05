from django.db import models
from db import base_model
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser, base_model.BaseModel):
    '''用户模型'''
    user_exp = models.IntegerField(default=0, verbose_name='用户经验值')
    user_grade = models.SmallIntegerField(default=0, verbose_name='用户等级')

    class Meta:
        db_table = "olens_user"
        verbose_name = '用户'
        verbose_name_plural = verbose_name





