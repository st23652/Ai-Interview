# myapp/forms.py
from django import forms
from .models import CV, CustomUser, JobApplication
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Job, Application, Interview, SkillAssessment, Skill, SkillAssessmentResult
from .models import CVUpload
from .models import Candidate, Employer
from .models import Interview  # Import your Interview model
from .models import InterviewAnswer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = InterviewAnswer
        fields = ['answer_text']

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['title', 'description', 'scheduled_date']

class InterviewScheduleForm(forms.Form):
    interview_date = forms.DateField(widget=forms.SelectDateWidget)
    interview_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

class YourForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['occupation', 'date_of_birth', 'industry', 'currently_employed', 'current_company']
        widgets = {
            'industry': forms.Select(choices=Candidate.INDUSTRY_CHOICES),
        }

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'start_date', 'company_size', 'industry']
        widgets = {
            'company_size': forms.Select(choices=Employer.COMPANY_SIZE_CHOICES),
            'industry': forms.Select(choices=Employer.INDUSTRY_CHOICES),
        }
        
class SettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'bio', 'linkedin', 'github']

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CVUpload
        fields = ['cv']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

class SkillAssessmentForm(forms.ModelForm):
    class Meta:
        model = SkillAssessment
        fields = ['name', 'description', 'questions']

class TakeSkillAssessmentForm(forms.ModelForm):
    class Meta:
        model = SkillAssessmentResult
        fields = ['answers']

def get_custom_user_model():
    from .models import CustomUser
    return CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'bio', 'linkedin', 'github', 'user_type', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'is_candidate', 'is_employer', 
            'occupation', 'date_of_birth', 'industry', 
            'currently_employed', 'current_company', 
            'company_name', 'company_start_date', 'company_size', 'company_industry'
        ]

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['candidate_name', 'candidate_email', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }
    
class ApplicationForm(forms.ModelForm):
    job = forms.ModelChoiceField(queryset=Job.objects.all(), empty_label="Select a job", widget=forms.Select)
    
    class Meta:
        model = Application
        fields = ['job', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_employer = forms.BooleanField(required=False)
    is_candidate = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'is_employer', 'is_candidate', 'company_name', 'industry', 'starting_date', 'company_size', 'phone_number', 'occupation', 'date_of_birth', 'is_employed']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class ProfileForm(forms.ModelForm):
    # Define the industry choices
    industry_choices = [
        'Technology',
        'Finance',
        'Healthcare',
        'Education',
        'Manufacturing',
        'Retail',
        'Hospitality',
        'Other'
    ]

    # Define the fields in the form
    industry = forms.ChoiceField(choices=[(i, i) for i in industry_choices], required=False)

    class Meta:
        model = Profile
        fields = ['occupation', 'profile_picture', 'date_of_birth', 'industry', 'currently_employed', 'current_company',
                  'company_name', 'company_start_date', 'company_size', 'company_industry']
        
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    country_code = forms.ChoiceField(choices=[('+1', 'US'), ('+44', 'UK')])  # Example choices
    user_type = forms.ChoiceField(choices=[('candidate', 'Candidate'), ('employer', 'Employer')])
    occupation = forms.CharField(required=False)
    candidate_industry = forms.CharField(required=False)
    experience = forms.IntegerField(required=False)
    cv = forms.FileField(required=False)
    company = forms.CharField(required=False)
    employer_industry = forms.CharField(required=False)
    years_open = forms.IntegerField(required=False)
    photo = forms.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'candidate':
            if not cleaned_data.get('occupation'):
                raise forms.ValidationError('Please enter your occupation.')
            if not cleaned_data.get('candidate_industry'):
                raise forms.ValidationError('Please enter your industry.')
        elif user_type == 'employer':
            if not cleaned_data.get('company'):
                raise forms.ValidationError('Please enter your company name.')
            if not cleaned_data.get('employer_industry'):
                raise forms.ValidationError('Please enter your employer industry.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user
    
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'occupation', 'date_of_birth', 'industry', 
            'currently_employed', 'current_company'
        ]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'company_name', 'company_start_date', 'company_size', 
            'company_industry', 'years_in_business', 'website', 
            'description', 'location'
        ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'description', 'experience', 'job_type', 'salary', 'deadline']

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['job', 'candidate_name', 'resume']

