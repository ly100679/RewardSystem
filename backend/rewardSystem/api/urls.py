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
    path('file', views.projectFile, name='projectFile'),
    path('submitfile', views.submitfile, name='submitfile'),
    path('competitionFile', views.competitionFile, name='competitionFile'),
    path('expertProjectGrade', views.expertProjectGrade, name='expertProjectGrade'),
    path('schoolProjectGrade', views.schoolProjectGrade, name='schoolProjectGrade')
]