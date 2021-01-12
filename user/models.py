from django.shortcuts import reverse
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Create your models here.
class Facalaty(models.Model):
    facalaty = models.CharField(max_length=100)
    def __str__(self):
        return self.facalaty

class Department(models.Model):
    department = models.CharField(max_length=75)
    facalaty = models.ForeignKey(Facalaty,on_delete=models.CASCADE)
    def __str__(self):
        return self.department

class StudentInfo(models.Model):
    CHOICES = (
        ('First Year','First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
        ('Fivth Year', 'Fivth Year'),
        ('Sixth Year', 'Sixth Year')

    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12,unique=True)
    faculty_name = models.ForeignKey(Facalaty,on_delete=models.CASCADE)
    department_name = models.ForeignKey(Department,on_delete=models.CASCADE)
    level = models.CharField(max_length=25,choices=CHOICES)
    profile_pic = models.ImageField(upload_to='profile_images')
    bio = models.TextField(blank=True)
    slug = models.SlugField(unique=True,blank=True)

    def get_absolute_url(self):
        return reverse('user:student_profile_search',kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user.username}')
        super(StudentInfo, self).save(*args, **kwargs)

    def __str__(self):
        return (self.user.username)

class ProfessorInfo(models.Model):
    CHOICES = [(str(i.department),str(i.department)) for i in Department.objects.all()]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12,unique=True)
    bio = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    degree_of_doctorate = models.CharField(max_length=100)
    departments_teach_to = MultiSelectField(choices=CHOICES)
    profile_pic = models.ImageField(upload_to='profile_images')
    slug = models.SlugField(unique=True,blank=True)

    def get_absolute_url(self):
        return reverse('user:professor_profile_search',kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user.username}')
        super(ProfessorInfo, self).save(*args, **kwargs)

    def __str__(self):
        return (self.user.username)

class ProfessorApprove(models.Model):
    professor = models.OneToOneField(ProfessorInfo,on_delete=models.CASCADE)
    def __str__(self):
        return self.professor.user.username
class Courses(models.Model):
    professor = models.ForeignKey(ProfessorInfo,on_delete=models.CASCADE)
    course_title = models.CharField(max_length= 35)
    course_description = models.TextField()
    course_pic = models.ImageField(upload_to='courses_pics')
    course_url = models.URLField()
    course_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True,blank=True)
    def video(self):
        url = self.course_url.split('com')
        url = url[0]+'com/embed'+url[1]
        return url
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.course_title}_{self.professor.user.username}')
        super(Courses, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user:course_details',kwargs={'slug':self.slug})

    def __str__(self):
        return self.course_title

class StudentsTasks(models.Model):
    student = models.ForeignKey(StudentInfo,on_delete=models.CASCADE)
    professor = models.ForeignKey(ProfessorInfo,on_delete=models.CASCADE)
    task = models.FileField(upload_to='students_tasks')
    def __str__(self):
        return f'{self.professor.user.username}_task_{self.task.name}'

