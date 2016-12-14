from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import sys


class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
       Creates and saves a User with the given username, email and password.
       """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    stripe_id = models.CharField(max_length=40, default='')
    subscription_end = models.DateTimeField(default=timezone.now)
    objects = AccountUserManager()

    def is_subscribed(self, magazine):
        #return True
        print >> sys.stderr, "this is magazine", magazine
        sys.stderr.flush()

        #try:
            #purchase = self.purchases.get(magazine__pk=magazine.pk)

        purchase = self.purchases.filter(magazine__pk=magazine.pk).first()
        #except Exception as e:
        #except ObjectDoesNotExist:
            #print type(e)
        #    return False
        print "purchase:",purchase
        if purchase is None:
            return False
        print >> sys.stderr, "this is purchase", purchase
        sys.stderr.flush()

        if purchase.subscription_end > timezone.now():
            return True


        return False

    def sub_end(self, magazine):
        print >> sys.stderr, "this is magazine", magazine
        sys.stderr.flush()

        purchase = self.purchases.filter(magazine__pk=magazine.pk).first()
        purchase_end = purchase.subscription_end
        print >> sys.stderr, "sub_end:purchase:",purchase_end

        return purchase_end
