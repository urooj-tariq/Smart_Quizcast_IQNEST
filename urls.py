from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   
       path('', views.welcome, name='welcome'),
       path('login/', views.login, name='login'),
       path('register/', views.register, name='register'),
       path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
       path('rating/', views.rating, name='rating'), 
       path('logout/',views.logout_view,name='logout'),
       path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
       path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
       path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
       path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
       path('instructor_dashboard/',views.instructor_dashboard,name='instructor_dashboard'),
        path('profile/', views.profile_view, name='profile'),
          path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
]



