from django.conf.urls import url
from django.urls import include
from rest_framework import serializers, viewsets, routers


from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from weblog.models import Blog
from weblog.models import Author
from weblog.models import Entry
from polls.models import Question
from polls.models import Choice


class LogEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LogEntry
        fields = [
            'id', 
            'action_time', 
            'user', 
            'content_type', 
            'object_id', 
            'object_repr', 
            'action_flag', 
            'change_message', 
        ]

class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer

class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id', 
            'name', 
            'content_type', 
            'codename', 
        ]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id', 
            'name', 
        ]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'password', 
            'last_login', 
            'is_superuser', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'is_staff', 
            'is_active', 
            'date_joined', 
        ]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = [
            'id', 
            'app_label', 
            'model', 
        ]

class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = [
            'session_key', 
            'session_data', 
            'expire_date', 
        ]

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'id', 
            'name', 
            'tagline', 
        ]

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id', 
            'name', 
            'email', 
        ]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = [
            'id', 
            'blog', 
            'headline', 
            'body_text', 
            'pub_date', 
            'mod_date', 
            'number_of_comments', 
            'number_of_pingbacks', 
            'rating', 
        ]

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 
            'question_text', 
            'pub_date', 
        ]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'id', 
            'question', 
            'choice_text', 
            'votes', 
        ]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


router = routers.DefaultRouter()

router.register(r'logentries', LogEntryViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'contenttypes', ContentTypeViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]