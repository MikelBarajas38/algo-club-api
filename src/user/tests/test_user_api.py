"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """
    Helper function to create a user.
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the public features of the user API (unauthenticated).
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful.
        """

        payload = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_email_exists_error(self):
        """
        Test creating a user that already exists fails.
        """

        payload = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'name': 'Test Name'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password_error(self):
        """
        Test creating a user with a password that is too short fails.
        """

        payload = {
            'email': 'test@example.com',
            'password': '1234',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(email=payload['email'])
        self.assertFalse(user.exists())

