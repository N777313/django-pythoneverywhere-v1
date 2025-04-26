import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """
    Создаёт вопрос с текстом `question_text`, опубликованный на указанное количество дней
    от текущего времени. Отрицательные `days` — в прошлом, положительные — в будущем.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Если вопросов нет, должна выводиться соответствующая надпись.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Вопрос с датой публикации в прошлом должен отображаться.
        """
        question = create_question("Прошлый вопрос.", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Вопрос с датой публикации в будущем не должен отображаться.
        """
        create_question("Будущий вопрос.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        Даже если есть и прошедший, и будущий вопрос — показывается только прошедший.
        """
        past_question = create_question("Прошлый вопрос.", -30)
        create_question("Будущий вопрос.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question],
        )

    def test_two_past_questions(self):
        """
        Отображаются оба прошедших вопроса, отсортированные по дате.
        """
        question1 = create_question("Прошлый вопрос 1.", -30)
        question2 = create_question("Прошлый вопрос 2.", -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
