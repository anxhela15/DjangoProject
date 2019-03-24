from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project,File,Suggestion, Task , Profile, Todo, Application
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

class CreateProject(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('project_name','require_suggestion','description','subject','workers',)

    def __init__(self, *args, **kwargs):
        
        super(CreateProject, self).__init__(*args, **kwargs)
        
        self.fields["workers"].widget = CheckboxSelectMultiple()
        self.fields["workers"].queryset = Profile.objects.all()

class CreateTask(ModelForm):

    class Meta:
        model = Task
        fields = ('task_name', 'description', 'subject', 'deadline',)

    def __init__(self, *args, **kwargs):
        
        super(CreateTask, self).__init__(*args, **kwargs)


class NewTask(ModelForm):

    class Meta:
        model = Task
        fields = ('deployers', )

    def __init__(self, *args, **kwargs):
        
        super(NewTask, self).__init__(*args, **kwargs)
        
        self.fields["deployers"].widget = CheckboxSelectMultiple()
        self.fields["deployers"].queryset = Profile.objects.filter(search=True)



class CreateFile(forms.ModelForm):

	class Meta:
		model = File
		fields = ('file_name','file','description','subject',)

class CreateSuggestion(forms.ModelForm):

	class Meta:
		model = Suggestion
		fields = ('sfile_name','sfile','description','subject',)		


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'password1', 'password2', )		


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('skills', )


class ChoiceForm(forms.Form):
    MY_CHOICES = User.objects.all()
    my_choice_field = forms.ChoiceField(choices=MY_CHOICES)


class CreateToDo(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ('name','to_do',)

class CreateApplication(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('description',)
