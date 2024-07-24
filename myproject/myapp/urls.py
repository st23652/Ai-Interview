from django.urls import path
from . import views

urlpatterns = [
    path('jobs/new/', views.job_create_view, name='job_create'),
    path('candidates/new/', views.candidate_create_view, name='candidate_create'),
    path('interviews/new/<int:job_id>/<int:candidate_id>/', views.interview_create_view, name='interview_create'),
    path('interviews/<int:interview_id>/', views.interview_detail_view, name='interview_detail'),
]
