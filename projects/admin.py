from django.contrib import admin
from .models import Project, ProjectInvitation, Member

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectInvitation)
admin.site.register(Member)
