from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import *
import json

#unfinish

def login(request):
	ans = {
		'user': None,
		'errorCode': 2
	}
	if request.method == 'POST':
		body = json.loads(request.body)
		name = body.get('account', None)
		password = body.get('password', None)
		user = authenticate(username=name, password=password)
		if user is not None:
			auth.login(request, user)
			ans['user'] = user
			return ans
		else:
			return ans
	else:
		return ans

def loginStudent(request):
	resp = {
		'status': False,
		'errorCode': 2
	}
	body = json.loads(request.body)
	name = body.get('account', None)
	# check if account exist & account type right
	try:
		Student.objects.get(username=name)
	except:
		resp['errorCode'] = 1
		return HttpResponse(json.dumps(resp), content_type='application/json')
	# try login
	user = login(request)
	resp['errorCode'] = user['errorCode']
	if user['user'] is not None:
		try:
			user = Student.objects.get(pk=user['user'].id)
			resp['status'] = True
		except:
			resp['status'] = False
			resp['errorCode'] = 1
			auth.logout(request)
	return HttpResponse(json.dumps(resp), content_type='application/json')

def loginExpert(request):
	resp = {
		'status': False,
		'errorCode': 2
	}
	body = json.loads(request.body)
	name = body.get('account', None)
	# check if account exist & account type right
	try:
		Expert.objects.get(username=name)
	except:
		resp['errorCode'] = 1
		return HttpResponse(json.dumps(resp), content_type='application/json')
	# try login
	user = login(request)
	resp['errorCode'] = user['errorCode']
	if user['user'] is not None:
		try:
			user = Expert.objects.get(pk=user['user'].id)
			resp['status'] = True
		except:
			resp['status'] = False
			resp['errorCode'] = 1
			auth.logout(request)
	return HttpResponse(json.dumps(resp), content_type='application/json')

def loginCommittee(request):
	resp = {
		'status': False,
		'errorCode': 2
	}
	body = json.loads(request.body)
	name = body.get('account', None)
	# check if account exist & account type right
	try:
		Committee.objects.get(username=name)
	except:
		resp['errorCode'] = 1
		return HttpResponse(json.dumps(resp), content_type='application/json')
	# try login
	user = login(request)
	resp['errorCode'] = user['errorCode']
	if user['user'] is not None:
		try:
			user = Committee.objects.get(pk=user['user'].id)
			resp['status'] = True
		except:
			resp['status'] = False
			resp['errorCode'] = 1
			auth.logout(request)
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
		new_student.student_id = int(body['account'])
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

def getProjectID(project):
	competition = project.competition
	competition_id = str(competition.id).rjust(5, '1')
	project_id = str(project.id).rjust(8, '1')
	competition_acronym = competition.acronym
	return competition_acronym + competition_id + project_id

def project(request):
	if request.method == 'DELETE':
		resp = {
			'status': False
		}
		project_id = request.GET.get('id')
		print(233)
		try:
			project = Project.objects.get(pk=project_id)
			project.delete()
			resp['status'] = True
		except:
			pass
		return HttpResponse(json.dumps(resp), content_type='application/json')
	if request.method == 'GET':
		student_id = request.GET.get('studentID')
		try:
			student = Student.objects.get(student_id=student_id)
		except:
			return []
		projects = Project.objects.filter(author=student)
		resp = []
		for project in projects:
			tem = {
				'id': project.id,
				'projectName': project.name,
				'projectID': getProjectID(project),
				'projectPeriod': project.status
			}
			resp.append(tem)
		return HttpResponse(json.dumps(resp), content_type='application/json')
