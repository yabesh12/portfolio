from django.urls import path
from core import views

urlpatterns = [
	path('', views.home, name="home"),
	path('project-detail/<slug>', views.project_details, name="project_details"),
	path('ajax/send-email-message/', views.ajax_send_email_message, name="ajax_send_email_message"),
    
	# Download resume
	path('download-resume/', views.download_resume, name="download_resume"),

]