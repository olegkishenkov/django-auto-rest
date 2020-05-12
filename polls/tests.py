from django.test import TestCase

# Create your tests here.
from django.urls import reverse, NoReverseMatch

from polls.models import Question


class TestPollsViewSets(TestCase):
    # def test_question_read_many__api_does_not_exist(self):
    #     self.assertRaises(NoReverseMatch, reverse, viewname='question-list')
    #
    # def test_question_read_one__api_does_not_exist(self):
    #     question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
    #     self.assertRaises(NoReverseMatch, reverse, viewname='question-detail', args=[question.pk])
    #
    # def test_question_create__api_does_not_exist(self):
    #     self.assertRaises(NoReverseMatch, reverse, viewname='question-detail')
    #
    # def test_question_update__api_does_not_exist(self):
    #     question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
    #     self.assertRaises(NoReverseMatch, reverse, viewname='question-detail', args=[question.pk])
    #
    # def test_question_delete__api_does_not_exist(self):
    #     question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
    #     self.assertRaises(NoReverseMatch, reverse, viewname='question-detail', args=[question.pk])

    def test_question_read_many__api_exists(self):
        response = self.client.get(reverse('question-list'))
        self.assertEqual(response.status_code, 200)

    def test_question_read_one__api_exists__question_does_not_exist(self):
        invalid_pk = 1
        response = self.client.get(reverse('question-detail', args=[invalid_pk]))
        self.assertEqual(response.status_code, 404)

    def test_question_read_one__api_exists__question_exists(self):
        question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
        response = self.client.get(reverse('question-detail', args=[question.pk]))
        self.assertEqual(response.status_code, 200)

    def test_question_create__api_exists(self):
        data ={
            'question_text': 'How are you?',
            'pub_date': '1970-01-01 00:00:00',
        }
        response = self.client.post(reverse('question-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Question.objects.filter(**data))

    def test_question_update__api_exists__question_does_not_exist(self):
        invalid_pk = 1
        data = {
            'question_text': 'How are you?',
            'pub_date': '1970-01-01 00:00:00',
        }
        response = self.client.put(reverse('question-detail', args=[invalid_pk]), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Question.objects.filter(**data))

    def test_question_update__api_exists__question_exists(self):
        question = Question.objects.create(question_text='How are you?', pub_date='1970-01-01 00:00:00')
        data = {
            'question_text': 'What\'s up?',
            'pub_date': '1971-01-01 00:00:00',
        }
        response = self.client.put(
            reverse('question-detail', args=[question.pk]),
            data=data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Question.objects.filter(**data))

    def test_question_delete__api_exists__question_does_not_exist(self):
        invalid_pk = 1
        response = self.client.delete(reverse('question-detail', args=[invalid_pk]))
        self.assertEqual(response.status_code, 404)

    def test_question_delete__api_exists__question_exists(self):
        data = {
            'question_text': 'How are you?',
            'pub_date': '1970-01-01 00:00:00',
        }
        question = Question.objects.create(**data)
        response = self.client.delete(reverse('question-detail', args=[question.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Question.objects.filter(**data))
