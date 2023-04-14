from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_tender_notification_seller_email(request, customer_email, tender):
    message = render_to_string(
        template_name='emails/tender_notification_seller.html',
        context={
            'domain': get_current_site(request),
            'tender': tender,
        },
    )

    email = EmailMessage(
        subject='MyMarker: We have new tender for you',
        body=message,
        to=[customer_email, settings.EMAIL_HOST_USER],
    )

    email.content_subtype = 'html'
    email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
