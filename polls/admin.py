from django.contrib import admin

# Register your models here.
from polls.models import Poll, Tag, Question, Choice

admin.site.register(Poll)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Choice)
