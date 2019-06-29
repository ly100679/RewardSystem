from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import *
import json

#unfinish

def login(request):
	if request.method == 'POST':
		body = json.loads(request.body)
		name = body.get('account', None)
		password = body.get('password', None)
		user = authenticate(username=name, password=password)
		if user is not None:
			auth.login(request, user)
			return user
		else:
			return None
	else:
		return None

def loginStudent(request):
	resp = {
		'status': False
	}
	user = login(request)
	if user is not None:
		try:
			user = Student.objects.get(pk=user.id)
			resp['status'] = True
		except:
			resp['status'] = False
	return HttpResponse(json.dumps(resp), content_type='application/json')

def loginExpert(request):
	resp = {
		'status': False
	}
	user = login(request)
	if user is not None:
		try:
			user = Expert.objects.get(pk=user.id)
			resp['status'] = True
		except:
			resp['status'] = False
	return HttpResponse(json.dumps(resp), content_type='application/json')

def loginCommittee(request):
	resp = {
		'status': False
	}
	user = login(request)
	if user is not None:
		try:
			user = Committee.objects.get(pk=user.id)
			resp['status'] = True
		except:
			resp['status'] = False
	return HttpResponse(json.dumps(resp), content_type='application/json')

def register(request):
	resp = {
		'status': False,
		'errorCode': 2
	}
	if request.method == 'POST':
		body = json.loads(request.body)
		try:
			new_student = Student.objects.create_user(username=body['account'], password=body['password'], email=body['email'])
		except:
			resp['errorCode'] = 1
			return HttpResponse(json.dumps(resp), content_type='application/json')
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
		resp['status'] = True
		return HttpResponse(json.dumps(resp), content_type='application/json')
	return HttpResponse(json.dumps(resp), content_type='application/json')