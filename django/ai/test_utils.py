import os
import tempfile
import simplejson

from django.test import TestCase

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

def create_user(username, password, first_name=None, last_name=None, email=None, is_staff=False):
    user = User.objects.create(username=username, is_staff=is_staff, is_superuser=is_staff, email=email)
    if first_name: user.first_name = first_name
    if last_name: user.last_name = last_name
    user.set_password(password)
    user.save()

    client = Client()
    client.login(username=username, password=password)
    return (user, client)

class ExtendedTestCase(TestCase):
    def assertFilesEqual(self, file_handle_1, file_handle_2):
        b1 = file_handle_1.read()
        b2 = file_handle_2.read()
        while b1 != "" and b2 != "" and b1 == b2:
            b1 = file_handle_1.read()
            b2 = file_handle_2.read()
        if b1 != b2:
            raise AssertionError('Files are not equal')

    def getJSON(self, url, client, token_key=None):
        if token_key:
            response = client.get(url, HTTP_ACCEPT='application/json', HTTP_AUTHORIZATION='Token ' + token_key)
        else:
            response = client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
        return simplejson.loads(response.content)

    def deleteJSON(self, url, client):
        '''Yes, even DELETE calls can return JSON'''
        response = client.delete(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
        return simplejson.loads(response.content)

    def postJSON(self, url, data, client):
        response = client.post(url, simplejson.dumps(data), content_type='application/json',  HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
        return simplejson.loads(response.content)

    def postFormAcceptJSON(self, url, data, client):
        response = client.post(url, data,  HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
        return simplejson.loads(response.content)

    def putJSON(self, url, data, client):
        response = client.put(url, simplejson.dumps(data), content_type='application/json', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
        return simplejson.loads(response.content)

    def assertEmptyString(self, value):
        if value != '':
            raise AssertionError('"%s" is not an empty string' % value)

    def assertResponseStatus(self, response, status):
        self.assertEqual(response.status_code, status)

def _is(value):
    return value != None and value != ""
def _not(value):
    return value == None or value == ""
