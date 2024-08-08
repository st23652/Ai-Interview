from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from .models import InterviewAnswer, Interview, InterviewAnswer, Job, CVUpload, Profile, Sector, Question, CandidateResponse, SkillAssessment
from .forms import CVForm, CandidateProfileForm, JobApplicationForm, JobForm, ProfileForm, SettingsForm, InterviewScheduleForm, CustomUserCreationForm, InterviewForm, SkillAssessmentForm, UserRegistrationForm, YourForm
from .models import Question
from .forms import AnswerForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Interview
from .serializers import ProfileSerializer
from .forms import ProfilePictureForm
from django.views.decorators.csrf import csrf_exempt

def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to a page where you list jobs
        else:
            print(form.error)
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})

@csrf_exempt
def save_answers(request, interview_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            interview = Interview.objects.get(id=interview_id)
            for question_text, answer in data.items():
                # Find the question object
                question = Question.objects.get(text=question_text)
                # Save the answer
                InterviewAnswer.objects.create(interview=interview, question=question, answer=answer)
            return JsonResponse({'message': 'Responses saved successfully.'}, status=200)
        except Interview.DoesNotExist:
            return JsonResponse({'error': 'Interview not found.'}, status=404)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def profile_view(request):
    profile = request.user.profile  # Assuming the user has a one-to-one relationship with the Profile model

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.error)
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'user': request.user})

def interview_questions(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)
    if request.method == 'POST':
        # Assuming answers are submitted via POST request
        answers = request.POST.get('answers')
        interview.answers = answers
        interview.completed = True
        interview.save()
        return redirect('interview_complete', interview_id=interview.id)
    return render(request, 'interview.html', {'interview': interview})

def question_set(request, set_name):
    questions = Question.objects.filter(question_set=set_name)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.save()
            return redirect('interview_questions')
        else:
            print(form.error)
    else:
        form = AnswerForm()
    return render(request, 'question_set.html', {'questions': questions, 'form': form})

def skill_assessment_detail(request, pk):
    assessment = get_object_or_404(SkillAssessment, pk=pk)
    context = {'assessment': assessment}
    return render(request, 'skill_assessment_detail.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        else:
            print(form.error)
    else:
        form = ProfileForm(instance=profile)

    industry_choices = ProfileForm.industry_choices

    return render(request, 'edit_profile.html', {'form': form, 'industry_choices': industry_choices})

def skill_assessment_result(request, pk):
    assessment = get_object_or_404(SkillAssessment, pk=pk)
    context = {'assessment': assessment}
    return render(request, 'skill_assessment_result.html', context)

def skill_assessment_take(request, pk):
    assessment = get_object_or_404(SkillAssessment, pk=pk)
    context = {'assessment': assessment}
    return render(request, 'skill_assessment_take.html', context)

def skill_assessment_create(request):
    if request.method == "POST":
        # Handle form submission
        form = SkillAssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Skill assessment created successfully!")
        else:
            print(form.error)
    else:
        form = SkillAssessmentForm()
    return render(request, 'skill_assessment_create.html', {'form': form})

def skill_assessment_list(request):
    assessments = SkillAssessment.objects.all()
    return render(request, 'skill_assessment_list.html', {'assessments': assessments})

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful upload
        else:
            print(form.error)
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profile.html', {'form': form})

def interview(request):
    interviews = Interview.objects.all()
    return render(request, 'interview.html', {'interviews': interviews})

def add_interview(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('interview_list')
        else:
            print(form.error)
    else:
        form = InterviewForm()
    return render(request, 'add_interview.html', {'form': form})

def add_candidate(request):
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
        else:
            print(form.error)
    else:
        form = CandidateProfileForm()
    return render(request, 'add_candidate.html', {'form': form})

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

@login_required
def interview_list(request):
    sectors = Sector.objects.all()
    return render(request, 'interview_list.html', {'sectors': sectors})

@login_required
def interview_detail(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)
    questions = Question.objects.filter(sector=sector).order_by('order')
    if request.method == 'POST':
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer:
                CandidateResponse.objects.create(
                    candidate=request.user,
                    question=question,
                    answer=answer
                )
        return redirect('interview_complete')
    return render(request, 'interview_detail.html', {'sector': sector, 'questions': questions})

@login_required
def interview_schedule(request):
    if request.method == 'POST':
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('interview_list')
        else:
            print(form.error)
    else:
        form = InterviewScheduleForm()
    return render(request, 'interview_schedule.html', {'form': form})

@login_required
def interview_complete(request):
    return render(request, 'interview_complete.html')

@csrf_protect
def my_protected_view(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            return redirect('success_url')
        else:
            print(form.error)
    else:
        form = YourForm()
    return render(request, 'your_template.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registration successful.'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def csrf_failure(request, reason=""):
    return render(request, '403_csrf.html', status=403)

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
def update_settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated successfully.')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error(s) below.')
            print(form.error)
    else:
        form = SettingsForm(instance=request.user)
    return render(request, 'settings.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            print(form.error)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def employer_dashboard(request):
    if request.user.profile.is_employer:
        jobs = Job.objects.filter(profile__company_name=request.user.profile.company_name)
        cv_uploads = CVUpload.objects.filter(job__in=jobs)
        context = {
            'jobs': jobs,
            'cv_uploads': cv_uploads,
        }
        return render(request, 'employer_dashboard.html', context)
    else:
        return redirect('home')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

@login_required
def job_details(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_details.html', {'job': job})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_details', pk=pk)
        else:
            print(form.error)
    else:
        form = JobForm(instance=job)
    return render(request, 'job_edit.html', {'form': form})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user.profile  
            application.save()
            return redirect('application_success')  
        else:
            print(form.error)
    else:
        form = JobApplicationForm()

    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'apply_job.html', context)

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

def candidate_create(request):
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
        else:
            print(form.error)
    else:
        form = CandidateProfileForm()
    return render(request, 'add_candidate.html', {'form': form})

@login_required
def job_postings_view(request):
    jobs = Job.objects.all()
    user_profile = request.user.profile
    profile_serializer = ProfileSerializer(user_profile)
    context = {
        'jobs': jobs,
        'user_profile_json': json.dumps(profile_serializer.data, cls=DjangoJSONEncoder),
    }

    if request.method == 'POST':
        if user_profile.is_employer:
            form = JobForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('job_postings')
            else:
                print(form.error)
        elif user_profile.is_candidate:
            form = CVForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('job_postings')
            else:
                print(form.error)
    else:
        job_form = JobForm() if user_profile.is_employer else None
        cv_form = CVForm() if user_profile.is_candidate else None
        context['job_form'] = job_form
        context['cv_form'] = cv_form

    return render(request, 'job_postings.html', context)

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
        else:
            print(form.error)
    else:
        form = JobForm()
    return render(request, 'job_create.html', {'form': form})

@login_required
def candidate_list(request):
    candidates = Profile.objects.filter(is_candidate=True)
    return render(request, 'candidate_list.html', {'candidates': candidates})

@login_required
def job_application_list(request):
    applications = CVUpload.objects.filter(user=request.user)
    return render(request, 'job_application_list.html', {'applications': applications})

@login_required
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(CustomUserCreationForm, email=email)
        if user:
            # Handle password reset logic
            return redirect('home')
    return render(request, 'reset_password.html')

def contact(request):
    if request.method == 'POST':
        # Handle form submission
        return HttpResponse("Contact form submitted successfully!")
    return render(request, 'contact.html')
