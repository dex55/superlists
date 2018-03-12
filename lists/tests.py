from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page


class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
