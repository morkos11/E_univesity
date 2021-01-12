from django.contrib import admin
from .models import StudentInfo, ProfessorInfo, ProfessorApprove, Department, Facalaty, Courses, StudentsTasks
# Register your models here.
admin.site.register(StudentInfo)
admin.site.register(ProfessorInfo)
admin.site.register(ProfessorApprove)
admin.site.register(Department)
admin.site.register(Facalaty)
admin.site.register(Courses)
admin.site.register(StudentsTasks)