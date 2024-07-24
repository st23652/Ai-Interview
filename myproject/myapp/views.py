from django.shortcuts import render, get_object_or_404, redirect
from .forms import JobForm, CandidateForm
from .models import Job, Candidate, Interview
from .utils import parse_resume, parse_job_description, conduct_interview

def job_create_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.parsed_description = parse_job_description(job.description)
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'job_create.html', {'form': form})

def candidate_create_view(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            candidate.parsed_resume = parse_resume(candidate.resume)
            candidate.save()
            return redirect('candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'candidate_create.html', {'form': form})

def interview_create_view(request, job_id, candidate_id):
    job = get_object_or_404(Job, id=job_id)
    candidate = get_object_or_404(Candidate, id=candidate_id)
    interview = Interview.objects.create(job=job, candidate=candidate)
    conduct_interview(interview)
    return redirect('interview_detail', interview_id=interview.id)

def interview_detail_view(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)
    return render(request, 'interview_detail.html', {'interview': interview})
