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

field = User._meta.get_field('username')
field.max_length = 254
