import time

from celery import shared_task

from core.utils.test_data_generators import account_generator


@shared_task
def test_task():
    time.sleep(5)


@shared_task
def accounts_generator_task(count, user_type):
    for _ in range(count):
        account_generator(user_type)
