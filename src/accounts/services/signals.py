from accounts.models import BuyerProfile, SellerProfile


def create_customer_profile(sender, instance, created: bool, **kwargs):
    if created:
        if instance.user_type == 0:
            buyer_profile = BuyerProfile(customer=instance)
            buyer_profile.save()
        elif instance.user_type == 1:
            seller_profile = SellerProfile(customer=instance)
            seller_profile.save()
