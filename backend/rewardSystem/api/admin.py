from django.contrib import admin
from .models import Expert, Student, Competition, School, Major

# Register your models here.
admin.site.register(Student)
admin.site.register(Expert)
admin.site.register(School)
admin.site.register(Major)
admin.site.register(Competition)