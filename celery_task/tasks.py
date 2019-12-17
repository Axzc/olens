from olens import settings
from celery import Celery
from django.core.mail import send_mail

import django
import os

# 环境的初始化
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "olens.settings")
django.setup()

app = Celery('celery_task.tasks', broker='redis://:123456@localhost:6379/7')


@app.task
def send_signup_active_mail(toemail, username, token):
    """
    :param toemail: 要发送的邮箱
    :param username:  收件人的用户名
    :param token:  加密后的userid
    :return:
    """

    subject = 'welcome messgae'
    message = ''
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [toemail]
    htmlmessage = '<h1>{} 感谢你在本站注册,请点击下面链接激活:' \
                  '</h1><br /><a href="http://127.0.0.1:8000/user/active/{}">' \
                  'http://127.0.0.1:8000/user/active/{}</a>'.format(username, token, token)

    # 发送邮件
    print('-----------------------')
    print(subject, message, sender, receiver)
    print('-----------------------')

    send_mail(subject, message, sender, receiver, html_message=htmlmessage)


@app.task
def send_forget_password_mail(toemail, username, token):
    """
    :param toemail: 要发送的邮箱
    :param username:  收件人的用户名
    :param token:  加密后的userid
    :return:
    """

    subject = "找回密码"
    message = "test"
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [toemail]
    htmlmessage = '<h1>{}您的账户正在找回密码,请点击下里面链接找回.(如非本人操作请及时修改密码)'\
                  '<h2><br /><a href="http://127.0.0.1:8000/user/resetpwd/{}"></h2>'\
                  'http://127.0.0.1:8000/user/resetpwd/{}'.format(username, token, token)

    send_mail(subject, message, sender, receiver, html_message=htmlmessage)






