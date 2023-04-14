import datetime

from celery import shared_task
from django.db.models import Q

from tenders.models import Tender


@shared_task
def tender_status_change_task():
    date = datetime.date.today()
    or_filters = (Q(end_day__lt=date) | Q(end_day=date)) & Q(status=Tender.StatusChoices.PUBLISHED)
    tenders = Tender.objects.filter(or_filters)

    for tender in tenders:
        tender.status = Tender.StatusChoices.EXECUTED
        tender.save()

        if tender.request.all().exists():
            tender_request = tender.request.all().order_by('total_price').first()
            tender_request.winner = True
            tender_request.save()
