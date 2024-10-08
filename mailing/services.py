import os.path
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
import random

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from mailing.models import Newsletter, Attempt, Blog

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
interval_dict = {'daily': 1, 'weekly': 7, 'monthly': 30}


def start_scheduler():
    '''
    Функция выбирает из базы все действующие и актуальные рассылки
    и на каждую устанавливает задачу планировщику
    :return:
    '''
    # if scheduler.running:
    #     return None
    work_status = ['created', 'launched']
    current_datetime = timezone.now()
    mailings = Newsletter.objects.filter(date_start__lte=current_datetime).filter(status__in=work_status)
    for mailing in mailings:  # цикл по рассылкам
        last_attempt = Attempt.objects.filter(newsletter=mailing).order_by('date_attempt').last()
        interval = interval_dict.get(mailing.frequency)
        if not last_attempt:  # если рассылка только создана (попыток нет) ставим планировщику задачу на текущее время
            scheduler.add_job(send_mailing, 'interval', days=interval, next_run_time=mailing.date_start, args=[mailing])
        else:  # определяем время запуска задачи для планировщика
            lost_days = (current_datetime - last_attempt.date_attempt).days  # переменная определяет сколько дней рассылки пропущено
            days_to_send = interval - lost_days % interval  # определяем сколько дней от последней попытки до следующей
            next_run_time = last_attempt.date_attempt + timezone.timedelta(days=lost_days + days_to_send)
            scheduler.add_job(send_mailing, 'interval', days=interval, next_run_time=next_run_time, args=[mailing])
    print(scheduler)
    print("Список задач планировщика:")
    scheduler.print_jobs()


def add_job_to_scheduler(mailing):
    '''
    Функция устанавливает задачу планировщику в случае создания новой
    или редактирования активной рассылки
    :param mailing:
    :return:
    '''
    interval = interval_dict.get(mailing.frequency)
    # если планировщик запущен, ставим задачу, иначе, запускаем его
    if scheduler.running:
        scheduler.add_job(send_mailing, 'interval', days=interval, next_run_time=mailing.date_start, args=[mailing])
    else:
        start_scheduler()


def send_mailing(mailing):
    '''
    Функция формирует сообщение и отправляет списку клиентов
    :param mailing:
    :return:
    '''
    message = EmailMessage(subject=mailing.message.topic,
                           body=mailing.message.body,
                           from_email=None,
                           to=[client.email for client in mailing.clients.all()])
    if mailing.message.media: # если в сообщении есть изображение, прикладываем к телу письма
        filename = mailing.message.media.file.name
        with open(filename, 'rb') as f:
            img_data = f.read()
            image = MIMEImage(img_data, name=os.path.basename(filename))
        message.attach(image)
    try:
        response = message.send(fail_silently=False)
        # если отправка рассылки прошла успешно, формируем и записываем в базу экземпляр попытки
        Attempt.objects.create(date_attempt=timezone.now(),
                               is_successful=True,
                               newsletter=mailing,
                               response=f"Успешно отправлено сообщений:  {response}")
    except smtplib.SMTPException as e:
        # если ответ почтового сервера вернулся с ошибкой формируем соответствующий экземпляр попытки
        Attempt.objects.create(date_attempt=timezone.now(),
                               is_successful=False,
                               newsletter=mailing,
                               response=e.strerror)


def get_cached_blogs():
    '''

    :return:
    '''
    if settings.CACHE_ENABLED:
        blog_list = cache.get('blog_list')
        if blog_list is None:
            blog_list = Blog.objects.all()
            cache.set('blog_list', blog_list)
    else:
        blog_list = Blog.objects.all()
        blog_list = random.sample(list(blog_list), 3)
    return blog_list
