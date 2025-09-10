from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Job(models.Model):
    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    ]

    employer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    salary = models.CharField(max_length=50, blank=True, null=True)
    experience_level = models.CharField(max_length=50)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)  
    perks = models.TextField(blank=True, null=True)  
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) 
    def __str__(self):
        return self.title



class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)   
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(blank=True, null=True)
    preferred_job_type = models.CharField(max_length=50, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    ], blank=True, null=True)
    preferred_location = models.CharField(max_length=100, blank=True, null=True)
    preferred_industry = models.CharField(max_length=100, blank=True, null=True)
    is_suspended = models.BooleanField(default=False)  
    def __str__(self):
        return self.user.username


    

class JobRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


    # company dashboard---------------



class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    team_size = models.PositiveIntegerField(default=1)
    description = models.TextField()

    def __str__(self):
        return self.name

class Report(models.Model):
    REPORT_TYPES = [
        ('Fake Job', 'Fake Job'),
        ('Scam', 'Scam'),
        ('Harassment', 'Harassment'),
        ('Other', 'Other'),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reported_by.username} - {self.report_type}"
