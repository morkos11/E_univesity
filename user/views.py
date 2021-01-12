from django.views.generic import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from . forms import SignupForm, StudentInfoForm, ProfessorInfoForm, CourseForm, StudentsTasksForm
from .models import ProfessorApprove, StudentInfo, ProfessorInfo, Courses
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    if request.user.is_authenticated:
       student = StudentInfo.objects.filter(user=request.user).exists()
       professor = ProfessorInfo.objects.filter(user=request.user).exists()
       trainers = ProfessorInfo.objects.filter(is_approved=True)[:4]
       courses = Courses.objects.all()[:3]
       no_students = StudentInfo.objects.all().count()
       no_courses = Courses.objects.all().count()
       no_prof = ProfessorInfo.objects.all().count()
       context ={
        'student':student,
        'professor':professor,
        'courses':courses,
        'trainers':trainers,
        'no_students':no_students,
        'no_courses':no_courses,
        'no_prof':no_prof
        }
    else:
        context = {
            'student':'student',
            'professor':'professor'
        }
    return render(request,'html/index.html',context)
def about(request):
    return render(request,'html/about.html')
def contact(request):
    user = request.user
    if User.objects.filter(username=user.username).exists():
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            email = user.email
            if subject == '' or message == '':
                messages.warning(request,'Failed to send the email, Please check the subject or message fields')
            else:
               send_mail(subject,f'{message} from {email} of {user.username}',settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER],fail_silently=True)
               messages.success(request,'Mail had sent successfully')
        context = {'user':True}
    else:
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            email = request.POST.get('email')
            name = request.POST.get('name')
            if subject == '' or message == '' or name == '' or email == '':
                messages.warning(request, 'Failed to send the email, Please check the subject or message fields')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'This email is already assigned, Please log in')
                send_mail(subject, f'Warning!\n we want to hint u that someone tried to use ur email to contact with the admin and the message was {message} and he used that name {name}\n if it was u then ignore that mail if it was not u please check ur account\nNote:that message did not sent to the admin',
                          settings.EMAIL_HOST_USER,
                          [email], fail_silently=True)
                return redirect('contact')
            else:
                send_mail(subject, f'{message} from {email} of {name}\nNote:email from guest user', settings.EMAIL_HOST_USER,
                          [settings.EMAIL_HOST_USER],fail_silently=True)
        context = {'user':False}
    return render(request,'html/contact.html',context)


def complete_signup(request):
    return render(request, 'registration_stuff/completeSignup.html')
def signup_form_Page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('/Complete_Data')
    else:
        form = SignupForm()
    context = {'form':form}
    return render(request, 'registration_stuff/signup.html', context)
def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'registration_stuff/logout.html')
def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           login(request,user)
           return redirect('/')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'registration_stuff/login.html', context)
def user_signup(request):
    if request.method=='POST':
        form= StudentInfoForm(request.POST, request.FILES)
        if form.is_valid():
           form.save(commit=False)
           form.instance.user = request.user
           if request.FILES:
              form.profile_pic = request.FILES['profile_pic']
           form.save()
           return redirect('/')

    else:
        form = StudentInfoForm()
    context ={'form':form}
    return render(request, 'registration_stuff/studentSignup.html', context)
def professor_signup(request):
    if request.method=='POST':
        form= ProfessorInfoForm(request.POST, request.FILES)
        if form.is_valid():
           form.save(commit=False)
           form.instance.user = request.user
           if request.FILES:
              form.profile_pic = request.FILES['profile_pic']
           professor = form.save()
           ProfessorApprove.objects.create(professor=professor)
           return redirect('/')

    else:
        form = ProfessorInfoForm()
    context ={'form':form}
    return render(request, 'registration_stuff/professorSignup.html', context)


def student_profile_view(request):
    student = StudentInfo.objects.get(user=request.user)
    context ={
        'student':student,
              }
    return render(request, 'profiles/student_profile.html', context)
def professor_profile_view(request):
    professor = ProfessorInfo.objects.get(user=request.user)
    courses = Courses.objects.filter(professor=professor)
    context ={
        'professor': professor,
        'courses': courses
              }
    return render(request, 'profiles/professor_profile.html', context)
def course_details_view(request,slug):
    course = get_object_or_404(Courses,slug=slug)
    return render(request, 'courses/course-details.html', {'course':course})
def course_create_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            print('yup')
            user = request.user
            professor = ProfessorInfo.objects.get(user=user)
            form.save(commit=False)
            form.instance.professor = professor
            if request.FILES :
                form.course_pic = request.FILES['course_pic']
            form.save()
            messages.success(request,'Course had created')
        else:
            messages.warning(request,'An error had accoured')
    else:
        form = CourseForm()
        print('nope')
    context = {
        'form':form
    }
    return render(request,'courses/add_course.html',context)
            


def search_student(request,slug):
    student = get_object_or_404(StudentInfo, slug=slug)
    if request.method == 'POST':
        user_name = request.user.username
        subject = request.POST.get('subject')
        email = request.user.email
        message = request.POST.get('message')
        recipient_list = student.user.email
        current_site = 'http://127.0.0.1:8000/'
        if ProfessorInfo.objects.filter(user=request.user,is_approved=True).exists():
            user_type = 'Professor'
            url = 'Profile/Professor/'
            slug = slug
            full_url = current_site+url+slug
        elif StudentInfo.objects.filter(user=request.user).exists():
            user_type = 'Student'
            url = 'Profile/Student/'
            slug = slug
            full_url = current_site+url + slug
        else:
            user_type = 'Mr'
            url = 'Profile/Professor/'
            slug = slug
            full_url = current_site+url + slug
        message = f'Dear {student.user.username},\n{user_type} {user_name} had sent u this message.\nMessage: {message} and his email is {email}\nTo respond:{full_url}'
        if len(subject) < 1 or len(message) < 1:
            messages.warning(request,'Message did not send, Please check the subject or message fields')
        else:
          send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient_list],
            fail_silently=True
          )
          messages.success(request,'Message had sent successfully')
    return render(request, 'search_stuff/search_student.html', {'student': student})
def search_professor(request,slug):
    professor = get_object_or_404(ProfessorInfo, slug=slug)
    courses = Courses.objects.filter(professor=professor)
    if request.method == 'POST':
        user_name = request.user.username
        subject = request.POST.get('subject')
        email = request.user.email
        message = request.POST.get('message')
        recipient_list = professor.user.email
        current_site = 'http://127.0.0.1:8000/'
        if ProfessorInfo.objects.filter(user=request.user, is_approved=True).exists():
            user_type = 'Professor'
            url = 'Profile/Professor/'
            slug = slug
            full_url = current_site + url + slug
        elif StudentInfo.objects.filter(user=request.user).exists():
            user_type = 'Student'
            url = 'Profile/Student/'
            slug = slug
            full_url = current_site + url + slug
        else:
            user_type = 'Mr'
            url = 'Profile/Professor/'
            slug = slug
            full_url = current_site + url + slug
        message = f'Dear {professor.user.username},\n{user_type} {user_name} had sent u this message.\nMessage: {message} and his email is {email}\nTo respond:{full_url}'
        if len(subject) < 1 or len(message) < 1:
            messages.warning(request, 'Message did not send, Please check the subject or message fields')
        else:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_list],
                fail_silently=False
            )
            messages.success(request, 'Message had sent successfully')
    return render(request, 'search_stuff/search_professor.html', {'professor': professor,'courses':courses})
def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        if User.objects.filter(username=search).exists():
           user = User.objects.get(username=search)
           if ProfessorInfo.objects.filter(user=user).exists():
              professor = ProfessorInfo.objects.filter(user=user)
              context = {'professor': professor}
           elif StudentInfo.objects.filter(user=user).exists():
                student = StudentInfo.objects.filter(user=user)
                context = {'student': student}
           else:
               email = user.email
               context = {'unfinished':f'user profile not available his mail is {email} '}
        else:
            context={'bad_search':search}
    return render(request, 'search_stuff/search.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user = form.save()
            update_session_auth_hash(request, user)
            user_auth = authenticate(username=request.user.username,password=new_password)
            login(request,user_auth)
            messages.success(request,'Password had seccessfully changed you will receive an email')
            send_mail('Password change',f'your password had been changed your new password is {new_password}',settings.EMAIL_HOST_USER,[request.user.email]
                      ,fail_silently=True)
        else:
            messages.error(request,'An error happened and password had not change')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request,'reset_password/change_password.html',context)

def student_tasks_view(request):
    if request.method == 'POST':
        form = StudentsTasksForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            student = StudentInfo.objects.get(user=request.user)
            form.instance.student = student
            if request.FILES:
                form.task = request.FILES['task']
            form.save()
            messages.success(request,'Your file uploaded successfully')
            # return redirect('user:student_profile')
    else:
        form = StudentsTasksForm()
    context = {'form':form}
    return render(request,'profiles/student_upload_tasks.html',context)



class Update_professor(UpdateView):
    model = ProfessorInfo
    template_name = 'profiles/update_professor.html'
    fields = ['phone_number','degree_of_doctorate','bio','departments_teach_to','profile_pic']
    success_url = '/Professor_Profile'
class UpdateStudent(UpdateView):
    model = StudentInfo
    template_name = 'profiles/update_student.html'
    fields = ['phone_number','profile_pic','bio']
    success_url = '/Student_Profile'
class UpdateCourse(UpdateView):
    model = Courses
    template_name = 'courses/update_course.html'
    fields = ['course_title','course_description','course_pic','course_url']
    success_url = '/Professor_Profile'

