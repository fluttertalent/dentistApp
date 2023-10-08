from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, QuestionForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Score, Tip, User
from datetime import date, timedelta
from django.core.paginator import Paginator
import random
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.core import serializers
import numpy as np
import json



@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        print(username, password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error('email', 'Invalid email or password')
            return self.form_invalid(form)
        
def logoutView(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) 
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request, f"Account created Successfully!")
            return redirect('login')
        
    else:
        print('render')
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



class PatientsListJson(BaseDatatableView):
    model = User
    columns = ['id', 'first_name', 'last_name', 'email','gender', 'birthday', 'dental_disease']
    order_columns = ['id', 'first_name', 'last_name', 'email','gender', 'birthday', 'dental_disease']
    max_display_length = 100 

    def get_initial_queryset(self):
        return User.objects.filter(user_type='patient')

@login_required
def patients_list(request):
    if request.user.user_type == 'doctor':
        return render(request, 'patients_list.html')
    else:
        return HttpResponseForbidden()
    

class PatientDetailView(DetailView):
    model = User
    template_name = 'patient_detail.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])



@login_required(login_url='login')
def question_list(request):
    # Retrieve all questions
    question_list = Question.objects.all()

    # Create a dictionary of questions by kind
    questions_by_kind = {}
    for question in question_list:
        if question.kind not in questions_by_kind:
            questions_by_kind[question.kind] = []
        questions_by_kind[question.kind].append(question) 

    existing_answers = Answer.objects.filter(user_id=request.user.id, pub_date=date.today()).exists()
    message = ''
    if existing_answers:
        message = 'You have already answered the questions for today.'

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print(request.user)
        if form.is_valid():
            score = 0
            for question_id, answer_value in form.cleaned_data.items():
                answer = Answer(user_id=request.user.id if request.user.is_authenticated else None, question_id=question_id, value=answer_value, pub_date=date.today())
                answer.save()
                score = score + int(answer_value)
            
            scoreData = Score(user_id=request.user.id if request.user.is_authenticated else None, value=score, pub_date=date.today())
            scoreData.save()

            str = ""
            if(score <= 14):
                str = "Status is Low Risk."
            elif(score >=15 and score <= 28):
                str = "Status is Moderate Risk."
            else:
                str = "Status is High Risk."

            message = "Successfully Answered. Your Score is {score}.".format(score=score) + " " + str

            tips = Tip.objects.all()
            random_index = random.randint(0, len(tips) - 1)
            random_tip = tips[random_index]

            context = {
                'questions_by_kind': questions_by_kind,
                'form': form,   
                'existing_answers':1,
                'message' : message,
                'tip': random_tip
            }
            return render(request, 'question_list.html', context)
            # Redirect or perform further actions
        else:
            print('Invalid post data')
            message = "Invalid post data" 
            context = {
                'questions_by_kind': questions_by_kind,
                'form': form,   
                'message' : message
            }
            return render(request, 'question_list.html', context)
    else:
        form = QuestionForm()
    
    context = {
        'questions_by_kind': questions_by_kind,
        'form': form,   
        'existing_answers':existing_answers,
        'message' : message        
    }

    # Render the template with the paginated questions
    return render(request, 'question_list.html', context)

@login_required(login_url='login')
def daily_scores_list(request):
    all_scores = Score.objects.all().order_by('user', '-pub_date')
    for score in all_scores:
        status = ''
        if(score.value <= 14):
            status = "Low Risk"
        elif(score.value >=15 and score.value <= 28):
            status = "Moderate Risk"
        else:
            status = "High Risk"
        score.status = status        

    context = {
        'all_scores': all_scores,
    }
    return render(request, 'daily_scores_list.html', context)

# def daily_scores_list(request):
#     all_answers = Answer.objects.all().order_by('user', '-pub_date')
#     all_answers_json = serializers.serialize('json', all_answers)
#     return JsonResponse(all_answers_json, safe=False)

def home_view(request):
    # Get the total number of patients
    total_patients = User.objects.filter(user_type='patient').count()

    # Get the total number of answers
    total_answers = Answer.objects.count()

    # Get the average score of today scores of all patients
    today = date.today()
    today_scores = Score.objects.filter(pub_date=today)
    today_scores_avg = np.mean([score.value for score in today_scores])

    # Get the graph of every day's average of score values
    scores = Score.objects.all().order_by('pub_date')
    scores_dates = [score.pub_date for score in scores]
    scores_values = [score.value for score in scores]
    scores_avg = []
    days = []
    current_day = scores_dates[0]
    current_sum = 0
    count = 0
    for i in range(len(scores_dates)):
        if scores_dates[i] == current_day:
            current_sum += scores_values[i]
            count += 1
        else:
            scores_avg.append(current_sum / count)
            days.append(current_day.strftime('%Y-%m-%d'))
            current_day = scores_dates[i]
            current_sum = scores_values[i]
            count = 1
    scores_avg.append(current_sum / count)
    days.append(current_day.strftime('%Y-%m-%d'))

    context = {
        'total_patients': total_patients,
        'total_answers': total_answers,
        'today_scores_avg': today_scores_avg,
        'scores_avg': json.dumps({'days': days, 'scores_avg': scores_avg})
    }
    
    return render(request, 'home.html', context)
