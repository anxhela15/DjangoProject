from django.contrib import admin
from .models import Project,Deployment,Profile,File,Suggestion, Task, Todo, Application
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group

# Register your models here.

admin.site.register(Project)
admin.site.register(Deployment)
admin.site.register(Profile)
admin.site.register(File)
admin.site.register(Suggestion)
admin.site.register(Task)
admin.site.register(Todo)
admin.site.register(Application)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)        