# coding=utf-8

import re
import time
import string
import requests
from random import Random

from django.conf import settings

from rest_framework import status
from utils.constants import FB_GRAPH_API_PROFILE_URL, PROFILE_IMAGE_DIR


USING_AWS_S3 = getattr(settings, 'USE_AWS_S3', False)


class UtlRandom:
    '''
    Random # generation
    '''
    random = ""

    def __init__(self):
        self.random = Random(x=time.time())

    def random_str(self, n):
        return ''.join(self.random.choice(string.ascii_uppercase +
                                          string.digits) for _ in range(n))

    def random_num(self, b, e):
        return self.random.randint(b, e)

    def random_username(self, length):
        return ''.join(self.random.choice(string.lowercase) for i in range(length))

    def random_email(self, length):
        email_host = 'example.com'
        random_username = self.random_username(length)
        return random_username+'@'+email_host


class ErrorType(object):

    NOT_AUTHORIZED = status.HTTP_401_UNAUTHORIZED
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    SUCCESS = status.HTTP_200_OK
    MISSING_ATTRIBUTES = status.HTTP_206_PARTIAL_CONTENT
    NOT_MODIFIED = status.HTTP_304_NOT_MODIFIED
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    CONFLICT = status.HTTP_409_CONFLICT
    NOT_ACCEPTABLE = status.HTTP_406_NOT_ACCEPTABLE
    NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED


class ValidateFBAccessToken(object):

    def __init__(self, access_token, data):
        self.access_token = access_token
        self.data_to_validate = data

    def is_valid(self):
        result = False
        url = FB_GRAPH_API_PROFILE_URL + '?access_token=' + self.access_token
        r = requests.get(url)
        response = r.json()
        for key in self.data_to_validate.keys():
            result = True if self.data_to_validate[key] == response.get(key, None) else False
        return result


IDENTIFIER_REGEX = re.compile('^[\w\d_]+\.[\w\d_]+\.\d+$')


def format_image_url(expression):
    """
    format image url for api response
    :param expression:
    :return:
    """
    values = expression.split('.') if expression else []

    if len(values) > 0:
        extension = '.'+values[-1]
        image_phrase = expression.replace(extension, '')
        if USING_AWS_S3:
            # s3_url = "https://%s.s3.amazonaws.com/"%getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'beco')
            s3_url = "https://%s/"%getattr(settings, 'AWS_CDN_DOMAIN', 'cdn1.becoapp.in')
            if '/media/' in image_phrase:
                image_phrase.replace('/media/', s3_url)
            else:
                image_phrase = s3_url+image_phrase
        return [
                image_phrase,
                extension
            ]
    return []