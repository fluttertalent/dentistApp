from django.urls import path
from .views import login_view, signup_view, save_answers
from .views import QuestionList

urlpatterns = [
    path('login/', login_view),
    path('signup/', signup_view),
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('save_answers/', save_answers),
]
