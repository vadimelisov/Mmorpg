from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from members import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='members/logout.html'), name='logout'),
    path('signup/', views.sign_up, name='signup'),
    path('activation/', views.activation, name='activation')
]
