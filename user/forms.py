from django import forms
from .models import StudentInfo, ProfessorInfo, Courses, StudentsTasks
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(UserCreationForm,self).__init__(*args,**kwargs)
        for field in ['first_name','last_name','password1','password2','username']:
            self.fields[field].help_text = None
            self.fields[field].required = True
    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if check:
            raise ValidationError('Email already exists')
        return email
    class Meta():
        model=User
        fields=('first_name','last_name','username','email','password1','password2')

class StudentInfoForm(forms.ModelForm):
    class Meta():
        model= StudentInfo
        fields= ('phone_number','faculty_name','department_name','level','profile_pic')

class ProfessorInfoForm(forms.ModelForm):
    class Meta():
        model= ProfessorInfo
        fields= ('phone_number','degree_of_doctorate','bio','departments_teach_to','profile_pic')

class CourseForm(forms.ModelForm):
    class Meta():
        model = Courses
        fields = ('course_title','course_description','course_pic','course_url')

class StudentsTasksForm(forms.ModelForm):
    # professor = forms.CharField(help_text='Choice the professor name')
    class Meta():
        model = StudentsTasks
        fields = ('professor','task')
