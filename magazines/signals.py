import arrow
from django.conf import settings
import datetime

timenow = datetime.datetime.now()
print "signals123:",timenow

def subscription_created(sender, **kwargs):
    print "signals456:", timenow

    from paypal.standard.models import ST_PP_COMPLETED, ST_PP_CANCELLED, ST_PP_PENDING
    ipn_obj = sender
    print "ipn_obj.payment_status",ipn_obj.payment_status
    print "ipn_obj.pending_reason", ipn_obj.pending_reason
    print "ipn_obj.receiver_email", ipn_obj.receiver_email
    if ipn_obj.payment_status != ST_PP_COMPLETED:
        return
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        return

    print "subscription_created"
    print "ipn_obj.custom:", ipn_obj.custom
    print "kwargs:", kwargs
    magazine_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    subscription_end = arrow.now().replace(weeks=+4).datetime
    from .models import Purchase


    purchase = Purchase.objects.filter(user_id=user_id, magazine_id=magazine_id).first()
    print "purchase:",purchase
    if purchase:
        print "already purchased"
        sub_end = purchase.subscription_end

        print sub_end
        #subscription_end = sub_end.replace(weeks=+4).datetime
        subscription_end = sub_end + datetime.timedelta(days=28)
        print "subscription_end",subscription_end
        print "magazine_id:",magazine_id
        print "user_id:",user_id
        #Purchase.objects.update_or_create(magazine_id=magazine_id,

        #                        user_id=user_id,
                                #subscription_end=arrow.now().replace(weeks=+4).datetime)
        #                        subscription_end=subscription_end)
        purchase.subscription_end = subscription_end
        purchase.save()

    else:
        print "NOT already purchased"
        Purchase.objects.create(magazine_id=magazine_id,
                                user_id=user_id,
                                subscription_end=arrow.now().replace(weeks=+4).datetime)
                                #subscription_end=subscription_end)
    #subscription_end = arrow.now().replace(weeks=+4).datetime

    #print "subscription_end:",subscription_end

    #(purchase,created) = Purchase.objects.get_or_create(magazine_id=magazine_id,
    #                        user_id=user_id)


    #purchase.subscription_end = subscription_end
    #purchase.save()
    #print "created:",created
    #print "purchase:",purchase
    #print "purchase.subscription_end:",purchase.subscription_end
    #Purchase.subscription_end = subscription_end
    #Purchase.save()

def subscription_was_cancelled(sender, **kwargs):
    from paypal.standard.models import ST_PP_COMPLETED, ST_PP_CANCELLED
    ipn_obj = sender
    print "ipn_obj.payment_status", ipn_obj.payment_status
    if ipn_obj.payment_status != ST_PP_CANCELLED:
        return

    print "subscription_was_cancelled"
    ipn_obj = sender
    print "ipn_obj.custom:",ipn_obj.custom
    print "kwargs:",kwargs
    magazine_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    from .models import Purchase
    purchase = Purchase.objects.get(user_id=user_id, magazine_id=magazine_id)
    #purchase = Purchase.objects.filter(user_id=user_id, magazine_id=magazine_id).first()
    purchase.subscription_end = arrow.now().datetime
    purchase.save()

#import arrow
#from django.conf import settings
#import datetime

#print "signals123"

#def subscription_created(sender, **kwargs):
#    from paypal.standard.models import ST_PP_COMPLETED, ST_PP_CANCELLED, ST_PP_PENDING
#    ipn_obj = sender
#    print "ipn_obj.payment_status", ipn_obj.payment_status
#   print "ipn_obj.pending_reason", ipn_obj.pending_reason
#    print "ipn_obj.receiver_email", ipn_obj.receiver_email
#    magazine_id = ipn_obj.custom.split('-')[0]
#    user_id = ipn_obj.custom.split('-')[1]
#   from .models import Purchase
#    Purchase.objects.create(magazine_id=magazine_id,
#                            user_id=user_id,
#                            subscription_end=arrow.now().replace(weeks=+4).datetime)


#def subscription_was_cancelled(sender, **kwargs):
#    ipn_obj = sender
#    magazine_id = ipn_obj.custom.split('-')[0]
#    user_id = ipn_obj.custom.split('-')[1]
#    from .models import Purchase
#    purchase = Purchase.object.get(user_id=user_id, magazine_id=magazine_id)
#    purchase.subscription_end = arrow.now().datetime
#    purchase.save()