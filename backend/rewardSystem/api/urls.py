from django.urls import path
from . import views

urlpatterns = [
    path('login/student', views.loginStudent, name='loginStudent'),
    path('login/expert', views.loginExpert, name='loginExpert'),
    path('login/school', views.loginCommittee, name='loginCommittee'),
    path('register', views.register, name='register'),
    path('studentProject', views.project, name='project'),
    path('studentInfo', views.student, name='student'),
    path('competition', views.competition, name='competition'),
    path('file', views.projectFile, name='projectFile')
]