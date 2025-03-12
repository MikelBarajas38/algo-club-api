"""
Tests for contest API.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Contest

from contest.serializers import (
    ContestSerializer,
    ContestDetailSerializer
)


CONTEST_URL = reverse('contest:contest-list')


def detail_url(contest_id):
    """
    create and return a detail URL for a contest.
    """
    return reverse('contest:contest-detail', args=[contest_id])


def create_contest(platform_id, **params):
    """
    Helper function to create a sample contest.
    """
    defaults = {
        'name': 'Test Contest',
        'description': 'Test Description',
        'url': 'https://example.com/contest/1',
        'platform': 'C',
        'platform_id': platform_id
    }
    defaults.update(params)
    contest = Contest.objects.create(**defaults)
    return contest


class PublicContestApiTests(TestCase):
    """
    Test the publicly available contest API (unauthenticated).
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required.
        """
        res = self.client.get(CONTEST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContestApiTests(TestCase):
    """
    Test the private contest API (authenticated).
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'contestuser@example.com',
            'testpass1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_contests(self):
        """
        Test retrieving a list of contests.
        """
        create_contest('1')
        create_contest('2')

        contests = Contest.objects.all().order_by('id')
        serializer = ContestSerializer(contests, many=True)

        res = self.client.get(CONTEST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_contest_detail(self):
        """
        Test getting a contest detail.
        """
        contest = create_contest('1')
        serializer = ContestDetailSerializer(contest)

        url = detail_url(contest.id)
        res = self.client.get(url)

        self.assertEqual(res.data, serializer.data)

    def test_create_contest_as_basic_user_fails(self):
        """
        Test creating a contest as a basic user.
        """
        payload = {
            'name': 'Test Contest',
            'description': 'Test Description',
            'url': 'https://example.com/contest/1',
            'platform': 'C',
            'platform_id': '1'
        }

        res = self.client.post(CONTEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_contest_as_basic_user_fails(self):
        """
        Test updating a contest as a basic user.
        """
        contest = create_contest('1')

        payload = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'url': 'https://example.com/contest/2',
            'platform': 'O',
            'platform_id': '2'
        }

        url = detail_url(contest.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_contest_as_basic_user_fails(self):
        """
        Test deleting a contest as a basic user.
        """
        contest = create_contest('1')

        url = detail_url(contest.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class StaffContestApiTests(TestCase):
    """
    Test the staff contest API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'superuser@example.com',
            'testpass1234'
        )
        self.client.force_authenticate(self.user)

    def test_create_contest(self):
        """
        Test creating a contest.
        """
        payload = {
            'name': 'Test Contest',
            'description': 'Test Description',
            'url': 'https://example.com/contest/1',
            'platform': 'C',
            'platform_id': '1000'
        }

        res = self.client.post(CONTEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        contest = Contest.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(v, getattr(contest, k))

    def test_update_contest(self):
        """
        Test updating a contest.
        """
        contest = create_contest('1')

        payload = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'url': 'https://example.com/contest/2',
            'platform': 'O',
            'platform_id': '2000'
        }

        url = detail_url(contest.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        contest.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(v, getattr(contest, k))

    def test_delete_contest(self):
        """
        Test deleting a contest.
        """
        contest = create_contest('1')

        url = detail_url(contest.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Contest.objects.filter(id=contest.id).exists())
