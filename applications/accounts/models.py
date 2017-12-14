# coding=utf-8

from __future__ import unicode_literals
import requests
import json
import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from utils.constants import USER_ROLES, BECO_CUSTOMER


class UserRoles(models.Model):
    """
    Data model for user roles
    """

    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        verbose_name_plural = _('User Roles')

    def __unicode__(self):
        return self.name


class User(AbstractUser):

    """ Custom user model for every beco user. """

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    mobile = models.CharField(_('Mobile Number'),max_length=25, null=True, blank=True)
    gender = models.CharField(_('Gender'), choices=GENDER_CHOICES, max_length=25, null=True, blank=True)
    role = models.CharField(_('Role'), choices=USER_ROLES, max_length=25, default=BECO_CUSTOMER)
    profile_image_url = models.CharField(verbose_name=_('Profile Image URL'), max_length=255, null=True, blank=True)
    dob = models.DateField(verbose_name=_('DOB'), null=True, blank=True)
    roles = models.ManyToManyField(UserRoles, verbose_name=_('User Roles'), blank=True)

    class Meta:
        verbose_name_plural = _('Users')

    def __unicode__(self):
        return self.get_username()


# def mailchimp_subscribe_user(sender, instance, created, **kwargs):
#     if created:
#         send_user_register_email(instance)
#         url = settings.MAILCHIMP_API_ENDPOINT+'lists/%s/members'%(settings.MAILCHIMP_LIST_ID)
#         try:
#             email = instance.email
#             fname = instance.first_name
#             lname = instance.last_name
#
#             data = {
#                     "email_address": email,
#                     "status": "subscribed",
#                     "merge_fields": {
#                         "FNAME": fname,
#                         "LNAME": lname
#                     }
#                 }
#             resp = requests.post(url, data=json.dumps(data), auth=(settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_ACCESS_KEY))
#         except Exception as e:
#             print e
#         generate_referral_id(instance)
#
# def mailchimp_delete_user(sender, instance, **kwargs):
#
#     try:
#         email = instance.email
#         m = hashlib.md5()
#         m.update(email.encode('utf-8'))
#         email_md5 = m.hexdigest()
#         url = settings.MAILCHIMP_API_ENDPOINT+'lists/%s/members/%s/'%(settings.MAILCHIMP_LIST_ID, email_md5)
#         resp = requests.delete(url, auth=(settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_ACCESS_KEY))
#
#         a = PointData.objects.filter(user_id=instance.id).delete
#     except Exception as e:
#         print e
#
# post_save.connect(mailchimp_subscribe_user, sender=User)
# post_delete.connect(mailchimp_delete_user, sender=User)
#
field = User._meta.get_field('username')
field.max_length = 254
