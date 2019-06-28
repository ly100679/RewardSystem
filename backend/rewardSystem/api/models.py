from django.db import models
from django.contrib.auth.models import User
from .enum import ProjectType, Education, Category

class School(models.Model):
    name = models.CharField(max_length=200)

class Major(models.Model):
    name = models.CharField(max_length=200)

class Student(User):
    student_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    enroll_year = models.IntegerField()
    tel = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    education = models.CharField(
        max_length=50,
        choices=[(t, t.value) for t in Education],
        null=True, blank=True
    )
    contact_address = models.CharField(max_length=500, null=True, blank=True)

class Expert(User):
    name = models.CharField(max_length=100)

class Committee(User):
    name = models.CharField(max_length=200, null=True, blank=True)

class Competition(models.Model):
    name = models.CharField(max_length=200)
    start = models.DateField(auto_now=False, auto_now_add=False)
    pre_review = models.DateField(auto_now=False, auto_now_add=False)
    review = models.DateField(auto_now=False, auto_now_add=False)
    oral_defense = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False, auto_now_add=False)

class ExpertList(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

class Project(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    project_type = models.CharField(
        max_length=10,
        choices=[(t, t.value) for t in ProjectType],
        null=True, blank=True
    )
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    video = models.FileField(upload_to='project_video/', null=True, blank=True)
    category = models.CharField(
        max_length=200,
        choices=[(t, t.value) for t in Category],
        null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    innovation = models.TextField(null=True, blank=True)

class CoAuthor(models.Model):
    student_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    education = models.CharField(
        max_length=50,
        choices=[(t, t.value) for t in Education]
    )
    tel = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class FormalProject(models.Model):
    status = models.CharField(max_length=50)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    expert = models.ManyToManyField(
        Expert,
        through='Opinion',
        through_fields=('project', 'expert')
    )

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='project_file/')

class ProjectImg(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='project_img/')

class Opinion(models.Model):
    project = models.ForeignKey(FormalProject, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    opinion = models.TextField(null=True, blank=True)
