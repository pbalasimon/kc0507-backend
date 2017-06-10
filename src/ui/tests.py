from django.test import Client
from django.test import TestCase


class HomePageTest(TestCase):
    def test_home_page_for_not_logged_user(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="/login">Ingresar</a>')
