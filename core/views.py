from django.shortcuts import render
from django.http import HttpResponse
from core.models import PersonalDetail, ProjectDetail, ProjectDetailImage, ProjectCategory, Client
from datetime import date
from django.db.models import Subquery
from django.contrib import messages
from django.core.mail import EmailMessage
import threading
from threading import Thread
from django.core.mail import send_mail
from portfolio.settings import EMAIL_HOST_USER
from .utils import validate_email

# Create your views here.


def home(request):
    try:

        person = PersonalDetail.objects.filter(name__iexact="yabesh samuvel")
        if person.exists():

            person_obj = person.first()
            address = person_obj.address
            pincode = person_obj.pincode
            bg_image = person_obj.bg_image

            # Calculate Age
            person_age = person_obj.calculate_age

            # Get SEO projects
            seo_projects_objs = ProjectDetail.objects.filter(
                user=person_obj, project_category__iexact="SEO")
            print(seo_projects_objs)
            # Get Web projects
            web_projects_objs = ProjectDetail.objects.filter(
                user=person_obj, project_category__iexact="WEB")

            # Get other projects
            other_projects_objs = ProjectDetail.objects.filter(
                user=person_obj, project_category__iexact="others")

            # # Get SEO projects images
            # seo_projects_images = ProjectDetailImage.objects.filter(project_id__in=Subquery(seo_projects_objs.values('id')))
            # print(seo_projects_objs)
            # print(seo_projects_images)

            # # Get WEB projects images
            # web_projects_images = ProjectDetailImage.objects.filter(project_id__in=Subquery(web_projects_objs.values('id')))
            # print(web_projects_objs)
            # print(web_projects_images)

            # # Get Other projects images
            # other_projects_images = ProjectDetailImage.objects.filter(project_id__in=Subquery(other_projects_objs.values('id')))
            # print(other_projects_objs)
            # print(other_projects_images)

        context = {
            'age': person_age,
            'address': address,
            'pincode': pincode,
            'bg_image': bg_image,
            'seo_projects': seo_projects_objs,
            'web_projects': web_projects_objs,
            'other_projects': other_projects_objs,
        }
        return render(request, 'core/index.html', context)

    except Exception as e:
        print(e)
        person_age = 27

        context = {'age': person_age}
        return render(request, 'core/index.html', context)


def project_details(request, slug):

    try:
        project_image_objs = ProjectDetailImage.objects.prefetch_related(
            'project').filter(project__name__iexact=slug)
        print(project_image_objs)
        project_url = project_image_objs.first().project.url
        category = project_image_objs.first().project.project_category
        client = project_image_objs.first().project.client_name
        print(f"{client} - {category} - {project_image_objs}")
        project_date = project_image_objs.first().project.project_date
        project_description = project_image_objs.first().project.description
        context = {'project_images': project_image_objs, 'project_url': project_url, 'category': category,
                   'client': client,
                   'project_date': project_date,
                   'description': project_description}
        return render(request, 'core/project_details.html', context)

    except Exception as e:
        print(e)

        return render(request, 'core/project_details.html')


class EmailThread(threading.Thread):
    def __init__(self, subject, message, to):
        self.subject = subject
        self.message = message
        self.to = to
        threading.Thread.__init__(self)
        # super(self.__class__, self).__init__()

    def run(self):
        msg = EmailMessage(self.subject, self.message,
                           EMAIL_HOST_USER, self.to)
        print("mail sent")
        msg.send()


def ajax_send_email_message(request):
    if request.is_ajax:
        print("Ajax")
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        validate_email(email)
        message = f"{message}, Client email address is - {email}"
        print(message)
        to = ["samyabeshv@gmail.com", ]
        em = EmailThread(subject, message, to)
        em.start()

        clients = Client.objects.update_or_create(name=name,
                                                  defaults={'email': email, 'subject': subject, 'message': message})
        msg = "Message sent Successfully!. Will reach you ASAP."
        print(msg)

    else:
        msg = "Sorry, Message is not sent, Please try again!"

    # messages.success(request, f"Thankyou {name}, Message Sent successfully! I'll talk to you ASAP")
    # return render(request, 'core/index.html')
    return HttpResponse(msg)
