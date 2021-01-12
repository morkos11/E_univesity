from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('SignUp',views.signup_form_Page,name='signup'),
    path('LogOut',views.log_out,name='log_out'),
    path('LogIn',views.log_in,name='log_in'),
    path('Complete_Data',views.complete_signup,name='complete_signup'),
    path('Student',views.user_signup,name='user_signup'),
    path('Professor', views.professor_signup, name='professor_signup'),
    path('Student_Profile', views.student_profile_view, name='student_profile'),
    path('Professor_Profile',views.professor_profile_view,name='professor_profile'),
    path('Profile/Student/<slug:slug>',views.search_student,name='student_profile_search'),
    path('Profile/Professor/<slug:slug>', views.search_professor, name='professor_profile_search'),
    path('Course/<slug:slug>',views.course_details_view,name='course_details'),
    path('Update_Professor/<slug>',views.Update_professor.as_view(),name='update_professor'),
    path('Update_Student/<slug>', views.UpdateStudent.as_view(), name='update_student'),
    path('Update_course/<slug>',views.UpdateCourse.as_view(),name='course_update'),
    path('Update_password/',views.change_password,name='change_password'),
    path('Create_course',views.course_create_view,name='create_course'),
    path('search',views.search,name='search'),
    path('Upload_tasks',views.student_tasks_view,name='upload_tasks'),
]