from django.urls import path
from .views import home_view, logoutView, signup, LoginView

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logoutView, name='logout'),
    
]
