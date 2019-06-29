from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import Student, School, Major
import json

#unfinish
def loginStudent(request):
	if request.method == 'POST':
		resp = {
			'status': True
		}
		body = json.loads(request.body)
		name = body.get('account', None)
		password = body.get('password', None)
		user = authenticate(username=name, password=password)
		if user is not None:
			auth.login(request, user)
			resp['status'] = True
		else:
			resp['status'] = False
		return HttpResponse(json.dumps(resp), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'status': False}), content_type="application/json")

def register(request):
	if request.method == 'POST':
		body = json.loads(request.body)
		new_student = Student.objects.create_user(username=body['account'], password=body['password'], email=body['email'])
		# new_student = Student.objects.get(pk=new_student.id)
		new_student.name = body['name']
		new_student.student_id = body['student_id']
		new_student.enroll_year = int(body['inYear'])
		new_student.tel = body['phoneNumber']
		new_student.email = body['email']
		try:
			school = School.objects.get(name=body['department'])
		except:
			school = School(name=body['department'])
			school.save()
		try:
			major = Major.objects.get(name=body['major'])
		except:
			major = Major(name=body['major'])
			major.save()
		new_student.school = school
		new_student.major = major
		new_student.save()
		return HttpResponse(json.dumps(body), content_type='application/json')