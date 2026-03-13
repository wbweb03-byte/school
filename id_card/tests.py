
from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)