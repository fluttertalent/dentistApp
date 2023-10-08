from django.urls import path
from .views import home_view, logoutView, signup, LoginView, question_list, patients_list, PatientsListJson, PatientDetailView, daily_scores_list

urlpatterns = [
    path('', question_list, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logoutView, name='logout'),
    path('patients/list/', patients_list, name='patients_list'),    
    path('patients/list/json/', PatientsListJson.as_view(), name='patients_list_json'),
    path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('dailyscores/list/', daily_scores_list, name='daily_scores_list'),
    path('dashboard/', home_view, name='dashboard')
]
