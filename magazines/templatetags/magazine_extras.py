import uuid
from django import template
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

register = template.Library()


def paypal_form_for(magazine, user):
    html = ""
    if user.is_subscribed(magazine):
        html = "Subscribed!"
    else:
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "currency_code": "GBP",
            "cmd": "_xclick-subscriptions",
            "a3": magazine.price,
            "p3": 1,
            "t3": "M",
            "src": 1,
            "sra": 1,
            "item_name": magazine.name,
            "invoice": uuid.uuid4(),
            "notify_url": settings.PAYPAL_NOTIFY_URL,
            "return_url": "%s/paypal-return/" % settings.SITE_URL,
            "cancel_return": "%s/paypal-cancel/" % settings.SITE_URL,
            "custom": "%s-%s" % (magazine.pk, user.id)
        }
        print paypal_dict
        if settings.DEBUG:
            html = PayPalPaymentsForm(initial=paypal_dict, button_type='subscribe').render()#sandbox()
        else:
            html = PayPalPaymentsForm(initial=paypal_dict, button_type='subscribe').render()

    return html


register.simple_tag(paypal_form_for)

def mag_sub_expiry(magazine, user):
    sub_expiry = ""
    if user.is_subscribed(magazine):
        html1 = user.sub_end(magazine)
        html2 = str(html1.strftime('%d %B %Y'))


        if html2:
            sub_expiry = "Subscribed Until " + str(html2)
    else:
        sub_expiry = "Not Subscribed"

    return sub_expiry

register.simple_tag(mag_sub_expiry)