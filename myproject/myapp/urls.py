# myapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import save_answers
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('interviews/<int:interview_id>/save_answers/', save_answers, name='save_answers'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/', views.job_details, name='job_details'),  # Corrected from job_detail to job_details
    path('job/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('apply_job/', views.apply_job, name='apply_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('interviews/', views.interview_list, name='interview_list'),
    path('interview/<int:sector_id>/', views.interview_detail, name='interview_detail'),
    path('schedule/', views.interview_schedule, name='interview_schedule'),
    path('complete/', views.interview_complete, name='interview_complete'),
    path('candidate/create/', views.candidate_create, name='candidate_create'),
    path('add_candidate/', views.add_candidate, name='add_candidate'),
    path('add_interview/', views.add_interview, name='add_interview'),
    path('add_job/', views.add_job, name='add_job'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('interview/', views.interview, name='interview'),
    path('job_application_list/', views.job_application_list, name='job_application_list'),
    path('job_postings/', views.job_postings_view, name='job_postings'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('settings/', views.update_settings, name='settings'),
    path('skills/', views.skill_assessment_list, name='skill_assessment_list'),
    path('skills/create/', views.skill_assessment_create, name='skill_assessment_create'),
    path('skills/<int:pk>/', views.skill_assessment_detail, name='skill_assessment_detail'),
    path('skills/<int:pk>/result/', views.skill_assessment_result, name='skill_assessment_result'),
    path('skills/<int:pk>/take/', views.skill_assessment_take, name='skill_assessment_take'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
