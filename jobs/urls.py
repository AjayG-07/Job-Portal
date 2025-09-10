from django.urls import path
from .views import home,job_list,job_detail,job_seeker_dashboard, employer_dashboard,apply_job, save_job,company_profile,post_job, job_listings, edit_job, delete_job,manage_applications,update_application_status,signup_job_seeker, signup_employer,login_view, logout_view,profile_update,withdraw_application, remove_saved_job


urlpatterns = [
    path('', home, name='home'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('dashboard/', job_seeker_dashboard , name='job_seeker_dashboard'),
    path('employer-dashboard/', employer_dashboard , name='employer_dashboard'),
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('jobs/<int:job_id>/save/', save_job, name='save_job'),

    path('company_profile/', company_profile, name='company_profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('application/withdraw/<int:job_id>/', withdraw_application, name='withdraw_application'),
    path('saved-job/remove/<int:job_id>/', remove_saved_job, name='remove_saved_job'),
 

    path('post_job/', post_job, name='post_job'),
    path('job_listings/', job_listings, name='job_listings'),
    path('edit_job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    path('manage_applications/', manage_applications, name='manage_applications'),
    path('update_application_status/<int:application_id>/<str:status>/', update_application_status, name='update_application_status'),
   
    path('signup/job_seeker/', signup_job_seeker, name='signup_job_seeker'),
    path('signup/employer/', signup_employer, name='signup_employer'),

    path('login/', login_view , name='login'),
    path('logout/', logout_view , name='logout'),


   


]
