from django.db import models
from django.contrib.auth.models import Group,User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone
import datetime

# Create your models here.
class Heading(models.Model):
    content = RichTextField()
    
class Deployment(models.Model):
	d_name=models.CharField(max_length=50,default='DEFAULT VALUE')
	deployer = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
	no_deployments = models.IntegerField(default=0)
	def __str__(self):
		return self.d_name
	class Meta:
		permissions=(
 			("view_project","can see available projects"),
		)

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default="DEFAULT")
    no_deployments = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    notification = models.BooleanField(default=False)
    days = models.IntegerField(default=0)
    newtask = models.BooleanField(default=False)
    tasks = models.IntegerField(default=0)
    payment = models.IntegerField(default=0)
    payment_calculated = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    new_task = models.BooleanField(default=False)
    def __str__(self):
    	return self.username
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
    	if created:
    		Profile.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_user_profile(sender,instance,**kwargs):
    	instance.profile.save()

class Project(models.Model):
	project_name=models.CharField(max_length=100)
	deployer=models.ForeignKey(User,limit_choices_to={'groups__name': "Deployers"},on_delete=models.CASCADE,default=0)
	deployed = models.BooleanField(default=False)
	workers = models.ManyToManyField(Profile)
	require_suggestion = models.BooleanField(default=False)
	subject = models.CharField(max_length=100,default='DEFAULT')
	description = models.TextField(default="DEFAULT")
	new_suggestion = models.BooleanField(default=False)
	new_task = models.BooleanField(default=False)
	updated = models.BooleanField(default=False)
	version = models.FloatField(default=0)
	def __str__(self):
		return self.project_name + str(self.version) 

	class Meta:
		permissions=(
 			("view_project","can see available projects"),
 			("create_project", "can create new projects"),			
		)



class File(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
	file_name = models.CharField(max_length=100, default="DEFAULT")
	file=models.FileField(upload_to='accounts/static')
	subject = models.CharField(max_length=30, default="DEFAULT")
	description = models.TextField(default="DEFAULT")
	new_suggestion = models.BooleanField(default=False)	
	def __str__(self):
		return self.file_name

class Suggestion(models.Model):
	file = models.ForeignKey(File, on_delete=models.CASCADE, default=0)
	author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
	sfile_name=models.CharField(max_length=100, default="DEFAULT")
	sfile=models.FileField(upload_to='accounts/static')
	description = models.TextField(default="DEFAULT")
	creation_date = models.DateTimeField(default=timezone.now)
	confirmed = models.BooleanField(default=False)
	subject = models.CharField(max_length=30, default="DEFAULT")


class Task(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
	task_name = models.CharField(max_length=100, default="DEFAULT")
	deployers = models.ManyToManyField(Profile, blank=True)
	description = models.TextField()
	deadline = models.DateTimeField('deadline')
	finished = models.BooleanField(default=False)
	finishtime = models.DateTimeField('completed at', null=True, blank=True)
	creation_date = models.DateTimeField('created at', null=True, blank=True)
	def __str__(self):
		return self.task_name