from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from rest_framework.authtoken.models import Token
from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    # username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default='')
    # token = models.OneToOneField(Token, on_delete=models.CASCADE)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='M')
    birthday = models.DateField(default='2000-01-01')   
    DENTAL_DISEASE_CHOICES = (
        ('D', 'Dental caries'),
        ('P', 'Periodonitis'),
        ('G', 'Gingivitis'),
        ('N', 'None')
    )
    dental_disease = models.CharField(max_length=100, choices=DENTAL_DISEASE_CHOICES)
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,default='patient')    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'user_type', 'birthday','username']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    # def get_absolute_url(self):
    #     return reverse('patient_detail', args=[str(self.id)])

    def get_daily_answers(self):
        today = date.today()
        answers = Answer.objects.filter(user=self.id, pub_date__lte=today).order_by('-pub_date')

        return answers

class Question(models.Model):
    text = models.CharField(max_length=255)
    weight = models.IntegerField()
    kind = models.CharField(max_length=255)
    yes_no = models.BooleanField()
    options = models.JSONField(null=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField()
    pub_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.username} - {self.question.text}: {self.value}"
    
class Score(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    pub_date = models.DateField()

    def  __str__(self):
        return f"{self.user.username} - {self.pub_date}: {self.value}"
    
class Tip(models.Model):

    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.text}"
