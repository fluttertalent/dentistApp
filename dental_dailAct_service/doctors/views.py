from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

