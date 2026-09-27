from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('post/', views.job_post, name='job_post'),
    path('edit/<int:pk>/', views.job_edit, name='job_edit'),
    path('delete/<int:pk>/', views.job_delete, name='job_delete'),

    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('applicants/<int:pk>/', views.job_applicants, name='job_applicants'),
]