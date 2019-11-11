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
    '''
    发送注册激活邮件
    :return:
    '''

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






