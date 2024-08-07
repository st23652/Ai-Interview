from django.contrib import admin
from .models import Job, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'job_type', 'salary', 'deadline')
    search_fields = ('title', 'company_name', 'description')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_employer', 'is_candidate', 'company_name', 'industry')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_employer', 'is_candidate', 'company_name', 'industry', 'starting_date', 'company_size', 'phone_number', 'occupation', 'date_of_birth', 'is_employed')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

from .models import CVSubmission  # Import your model

# Register your model
@admin.register(CVSubmission)
class CVSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'job', 'submitted_at')  # Customize as per your model fields
    search_fields = ('name', 'email')
    list_filter = ('job', 'submitted_at')
    ordering = ('-submitted_at',)
