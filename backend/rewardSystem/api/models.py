from django.db import models
from django.contrib.auth.models import User
from .enum import *

class School(models.Model):
    name = models.CharField(max_length=200)

class Major(models.Model):
    name = models.CharField(max_length=200)

class Student(User):
    def __name__(self):
        return 'Student'
    student_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True)
    enroll_year = models.IntegerField(null=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    education = models.CharField(
        max_length=50,
        null=True, blank=True
    )
    contact_address = models.CharField(max_length=500, null=True, blank=True)

class Expert(User):
    name = models.CharField(max_length=100)

class Committee(User):
    name = models.CharField(max_length=200, null=True, blank=True)

class Competition(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=10, null=True, blank=True)
    start = models.DateField(auto_now=False, auto_now_add=False)
    pre_review = models.DateField(auto_now=False, auto_now_add=False)
    review = models.DateField(auto_now=False, auto_now_add=False)
    oral_defense = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField(null=True, blank=True)

class CompetitionFile(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    competition_file = models.FileField(upload_to='proje_competition_file/', max_length=500)

class ExpertList(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

class Project(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    # school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    project_type = models.CharField(
        max_length=100,
        null=True, blank=True
    )
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50
    )
    video = models.FileField(upload_to='project_video/', null=True, blank=True)
    category = models.CharField(
        max_length=200,
        null=True, blank=True
    )
    expert = models.ManyToManyField(
        Expert,
        through='Opinion',
        through_fields=('project', 'expert')
    )
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    innovation = models.TextField(null=True, blank=True)

class CoAuthor(models.Model):
    student_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    education = models.CharField(
        max_length=50,
        null=True, blank=True
    )
    tel = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='project_file/')

class ProjectImg(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='project_img/')

class Opinion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    opinion = models.TextField(null=True, blank=True)
