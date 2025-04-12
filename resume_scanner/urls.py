from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path ('joblist/', views.job_list, name='job_list'),
    path ('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path ('login/', views.login_view, name='login'),
    path ('signup/', views.signup_view, name='signup'),
path('logout/', views.logout_view, name='logout'),
path('fraud-check/', views.fraud_check_view, name='fraud_check'),
path('result/<int:pk>/', views.result_view, name='result_view'),
path('scoreboard/<int:job_id>/', views.scoreboard_view, name='scoreboard'),
]
