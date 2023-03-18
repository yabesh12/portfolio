from django.contrib import admin
from core.models import PersonalDetail, ProjectDetail,ProjectDetailImage, ProjectCategory, Client

# Register your models here.
admin.site.register(PersonalDetail)
admin.site.register(ProjectDetail)
admin.site.register(ProjectCategory)
admin.site.register(ProjectDetailImage)
admin.site.register(Client)