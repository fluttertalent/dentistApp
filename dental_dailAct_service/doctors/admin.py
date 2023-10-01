from django.contrib import admin
from .models import User
from .models import Question,Answer

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
