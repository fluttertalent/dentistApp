from django.contrib import admin
from .models import User
from .models import Question, Answer, Tip, Score

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tip)
admin.site.register(Score)