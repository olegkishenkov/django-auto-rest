from django.test import TestCase


# Create your tests here.
from rest_framework.reverse import reverse

from .models import Question


class TestAutorestPreView(TestCase):
    def test_question_list__api_installed(self):
        response = self.client.get(reverse('model-list', args=['questions']))
        self.assertEqual(response.status_code, 200)

    def test_question_create__api_installed(self):
        data = {
            'question_text': 'How are you?',
            'pub_date': '1970-01-01 00:00:00',
        }
        response = self.client.post(reverse('model-list', args=['question']), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Question.objects.filter(**data))

    def test_question_retrieve__api_installed__question_exists(self):
        question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
        response = self.client.get(reverse('model-detail', args=['question', question.pk]))
        self.assertEqual(response.status_code, 200)

    def test_question_retrieve__api_installed__question_does_not_exist(self):
        invalid_pk = 1
        response = self.client.get(reverse('model-detail', args=['question', invalid_pk]))
        self.assertEqual(response.status_code, 404)

    def test_question_update__api_installed__question_exists(self):
        question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
        data = {
            'question_text': 'What\'s up?',
            'pub_date': '1971-01-01 00:00:00',
        }
        response = self.client.put(
            reverse('model-detail', args=['question', question.pk]),
            data=data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Question.objects.filter(**data))

    def test_question_update__api_installed__question_does_not_exist(self):
        invalid_pk = 1
        data = {
            'question_text': 'How are you?',
            'pub_date': '1970-01-01 00:00:00',
        }
        response = self.client.put(reverse('model-detail', args=['question', invalid_pk]), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Question.objects.filter(**data))

    def test_question_destroy__api_installed__question_exists(self):
        data = {
            'question_text': 'How are you?',
            'pub_date': '1970-01-01 00:00:00',
        }
        question = Question.objects.create(**data)
        response = self.client.delete(reverse('model-detail', args=['question', question.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Question.objects.filter(**data))

    def test_question_destroy__api_installed__question_does_not_exist(self):
        invalid_pk = 1
        response = self.client.delete(reverse('model-detail', args=['question', invalid_pk]))
        self.assertEqual(response.status_code, 404)

    def test_question_list_api_not_installed(self):
        with self.settings(AUTOREST_NOT_INSTALLED=True):
            response = self.client.get(reverse('model-list', args=['questions']))
            self.assertEqual(response.status_code, 501)

    def test_question_create_api_not_installed(self):
        with self.settings(AUTOREST_NOT_INSTALLED=True):
            response = self.client.get(reverse('model-list', args=['questions']))
            self.assertEqual(response.status_code, 501)

    def test_question_retrieve_api_not_installed(self):
        with self.settings(AUTOREST_NOT_INSTALLED=True):
            arbitrary_pk = 1
            response = self.client.get(reverse('model-detail', args=['questions', arbitrary_pk]))
            self.assertEqual(response.status_code, 501)

    def test_question_update_api_not_installed(self):
        with self.settings(AUTOREST_NOT_INSTALLED=True):
            arbitrary_pk = 1
            response = self.client.get(reverse('model-detail', args=['questions', arbitrary_pk]))
            self.assertEqual(response.status_code, 501)

    def test_question_delete_api_not_installed(self):
        with self.settings(AUTOREST_NOT_INSTALLED=True):
            arbitrary_pk = 1
            response = self.client.get(reverse('model-detail', args=['questions', arbitrary_pk]))
            self.assertEqual(response.status_code, 501)