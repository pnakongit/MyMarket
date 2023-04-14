from core.servises.emails import send_tender_notification_seller_email


def sending_emails_start_tender(request, tender):
    email_list = tender.get_seller_email_for_mailing()
    if email_list:
        for email in email_list:
            send_tender_notification_seller_email(customer_email=email, request=request, tender=tender)
