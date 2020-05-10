from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class TestPollsViewSets(TestCase):
    def test_question_list__api_exists(self):
        response = self.client.get(reverse('question-list'))
        self.assertEqual(response.status_code, 200)