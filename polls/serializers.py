from rest_framework.serializers import HyperlinkedModelSerializer

from polls.models import Question


class QuestionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question_text',
            'pub_date',
        ]