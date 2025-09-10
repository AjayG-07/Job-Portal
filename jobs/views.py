from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job ,JobApplication, SavedJob, Profile,JobRecommendation,CompanyProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jobs.forms import ProfileUpdateForm,JobPreferencesForm,CompanyProfileForm,JobForm,SignupForm, LoginForm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout

# Create your views here.



def home(request):
    jobs = Job.objects.all().order_by('-date_posted')

    # Pagination: Show 3 jobs per page
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/home.html', {'page_obj': page_obj})







def signup_job_seeker(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)  
            messages.success(request, "Job Seeker account created successfully! Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'jobs/accounts/signup_job_seeker.html', {'form': form})


def signup_employer(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            CompanyProfile.objects.create(user=user)  
            messages.success(request, "Employer account created successfully! Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'jobs/accounts/signup_employer.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'jobs/accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')




def job_list(request):
    jobs = Job.objects.all()  
    
   
    search_query = request.GET.get('search', '')
    location_query = request.GET.get('location', '')
    job_type_query = request.GET.get('job_type', '')

    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    if job_type_query:
        jobs = jobs.filter(job_type=job_type_query)

  
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1) 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  

    job_types = Job.JOB_TYPES  

    return render(request, 'jobs/jobs.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'location_query': location_query,
        'job_type_query': job_type_query,
        'job_types': job_types,
    })






def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('job_seeker_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'jobs/profile_update.html', {'form': form})




def withdraw_application(request, job_id):
    application = get_object_or_404(JobApplication, job__id=job_id, user=request.user)
    application.delete()
    messages.success(request, "You have successfully withdrawn your application.")
    return redirect('job_seeker_dashboard')

def remove_saved_job(request, job_id):
    saved_job = get_object_or_404(SavedJob, job__id=job_id, user=request.user)
    saved_job.delete()
    messages.success(request, "Job removed from saved jobs.")
    return redirect('job_seeker_dashboard')


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)  
    return render(request, 'jobs/job_detail.html', {'job': job})


from django.contrib.auth.decorators import login_required

@login_required
def job_seeker_dashboard(request):
    return render(request, 'jobs/job_seeker_dashboard.html')


def job_seeker_dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    
    if request.method == 'POST' and 'profile_update' in request.POST:
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('job_seeker_dashboard')
    else:
        profile_form = ProfileUpdateForm(instance=profile)

    
    if request.method == 'POST' and 'preferences_submit' in request.POST:
        preferences_form = JobPreferencesForm(request.POST, instance=profile)
        if preferences_form.is_valid():
            preferences_form.save()
            messages.success(request, "Job preferences updated!")
            return redirect('job_seeker_dashboard')
    else:
        preferences_form = JobPreferencesForm(instance=profile)

    
    recommended_jobs = JobRecommendation.objects.filter(user=request.user).order_by('-score')

    
    applied_jobs = JobApplication.objects.filter(user=request.user)
    saved_jobs = SavedJob.objects.filter(user=request.user)

    return render(request, 'jobs/job_seeker_dashboard.html', {
        'profile': profile,
        'profile_form': profile_form,
        'preferences_form': preferences_form,
        'applied_jobs': applied_jobs,
        'saved_jobs': saved_jobs,
        'recommended_jobs': recommended_jobs,
    })



@login_required
def employer_dashboard(request):
    return render(request, 'jobs/employer_dashboard.html') 



@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)


    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        JobApplication.objects.create(user=request.user, job=job)
        messages.success(request, "Your application has been submitted successfully!")

    return redirect('job_detail', job_id=job.id)

@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    
    if SavedJob.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You have already saved this job.")
    else:
        SavedJob.objects.create(user=request.user, job=job)
        messages.success(request, "Job saved successfully!")

    return redirect('job_detail', job_id=job.id)






def recommend_jobs(user):
    user_profile = Profile.objects.get(user=user)
    user_skills = user_profile.skills if user_profile.skills else ""
    
   
    jobs = Job.objects.all()
    if user_profile.preferred_job_type:
        jobs = jobs.filter(job_type=user_profile.preferred_job_type)
    if user_profile.preferred_location:
        jobs = jobs.filter(location__icontains=user_profile.preferred_location)
    if user_profile.preferred_industry:
        jobs = jobs.filter(industry__icontains=user_profile.preferred_industry)

    job_descriptions = [job.description for job in jobs]

    vectorizer = TfidfVectorizer()
    all_texts = [user_skills] + job_descriptions
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    user_vector = tfidf_matrix[0]  
    job_vectors = tfidf_matrix[1:]  

    similarities = cosine_similarity(user_vector, job_vectors).flatten()
    recommended_jobs = sorted(zip(jobs, similarities), key=lambda x: x[1], reverse=True)

    
    JobRecommendation.objects.filter(user=user).delete()  
    for job, score in recommended_jobs[:5]: 
        JobRecommendation.objects.create(user=user, job=job, score=score)

    return recommended_jobs[:5]

    

   



def company_profile(request):
    profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('company_profile')
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, 'jobs/employer/company_profile.html', {'form': form, 'profile': profile})





@login_required
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('job_listings')
        else:
            messages.error(request, "Failed to post job. Please check your inputs.")
    else:
        form = JobForm()

    return render(request, 'jobs/employer/post_job.html', {'form': form})



@login_required
def job_listings(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'jobs/employer/job_listings.html', {'jobs': jobs})


@login_required
def edit_job(request, job_id):
    job = Job.objects.get(id=job_id, employer=request.user)
    
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_listings')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/employer/edit_job.html', {'form': form, 'job': job})


@login_required
def delete_job(request, job_id):
    job = Job.objects.get(id=job_id, employer=request.user)
    job.delete()
    return redirect('job_listings')





@login_required
def manage_applications(request):


   
    jobs = Job.objects.filter(employer=request.user)
    applications = JobApplication.objects.filter(job__in=jobs)

    print("Logged-in employer:", request.user)
    print("Jobs posted by employer:", list(jobs.values('id', 'title')))
    print("Applications received:", list(applications.values('id', 'user_id', 'job_id', 'status')))

    if not jobs.exists():
        messages.warning(request, "You haven't posted any jobs yet.")

    if not applications.exists():
        messages.warning(request, "No job applications found.")

    return render(request, 'jobs/employer/manage_applications.html', {
        'applications': applications
    })




@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(JobApplication, id=application_id, job__employer=request.user)
    application.status = status
    application.save()
    messages.success(request, f"Application status updated to {status}.")
    return redirect('manage_applications')

