from celery import shared_task

from core.utils.test_data_generators import order_generator, product_generator


@shared_task
def products_generator_task(count):
    for _ in range(count):
        product_generator()


@shared_task
def orders_generator_task(count):
    for _ in range(count):
        order_generator()
