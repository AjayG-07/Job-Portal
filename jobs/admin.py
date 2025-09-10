
from django.contrib import admin
from .models import Job, JobApplication, SavedJob, Profile, JobRecommendation, CompanyProfile
from django.contrib.auth.models import User

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'job_type', 'date_posted', 'is_active')
    list_filter = ('job_type', 'is_active', 'date_posted')
    search_fields = ('title', 'company_name', 'location')
    actions = ['approve_jobs', 'deactivate_jobs']

    def approve_jobs(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected jobs have been approved.")
    approve_jobs.short_description = "Approve selected jobs"

    def deactivate_jobs(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected jobs have been deactivated.")
    deactivate_jobs.short_description = "Deactivate selected jobs"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'job__title')
    actions = ['mark_as_hired', 'mark_as_rejected']

    def mark_as_hired(self, request, queryset):
        queryset.update(status='Hired')
        self.message_user(request, "Selected applicants have been marked as Hired.")
    mark_as_hired.short_description = "Mark as Hired"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, "Selected applicants have been marked as Rejected.")
    mark_as_rejected.short_description = "Mark as Rejected"


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__username', 'job__title')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_job_type', 'preferred_location', 'preferred_industry')
    search_fields = ('user__username', 'preferred_location')


@admin.register(JobRecommendation)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'score', 'created_at')
    search_fields = ('user__username', 'job__title')


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'team_size')
    search_fields = ('name', 'industry', 'location')



