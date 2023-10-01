from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from doctors.models import User

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email address Or User name')
    

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username','password1', 'password2','user_type', 'birthday','gender','dental_disease')
    
    # Example of a custom field-level validation method
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        print(email)
        if email and User.objects.filter(email=email).exists():
            print('Email address has already been used')
            raise forms.ValidationError('Email address has already been used')
        if username and User.objects.filter(username=username).exists():
            print('Username has already been used')
            raise forms.ValidationError('Username has already been used')
        return email

    # Example of overriding the clean method for form-level validation
    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(cleaned_data)
    #     password1 = cleaned_data.get('password1')
    #     password2 = cleaned_data.get('password2')
    #     print(password1, password2)
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("The two password fields didn't match.")
    #     return cleaned_data
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        print(password2, password1)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
    
    