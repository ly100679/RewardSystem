from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import *
import json
from datetime import datetime

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
		# if student exist
		try:
			student = Student.objects.get(student_id=student_id)
		except:
			return HttpResponse(json.dumps({}), content_type='application/json')
		# if at least one competition
		try:
			competition = Competition.objects.order_by('-start')[0]
		except:
			return HttpResponse(json.dumps({}), content_type='application/json')
		projects = Project.objects.filter(author=student, competition=competition)
		project_id = request.GET.get('id', None)
		if project_id is not None:
			projects = []
			projects.append(Project.objects.get(pk=project_id))
		resp = {}
		data = []
		for project in projects:
			author = project.author
			tem = {
				'id': project.id,
				'projectName': project.name,
				'projectID': getProjectID(project),
				'projectPeriod': project.status,
				'nameOfWork': project.name,
				'classificationOfWork': project.project_type,
				'declarationOfWork': project.category,
				'overallDescriptionOfWork': project.description,
				'innovationPoint': project.innovation,
				'keyWord': project.keyword,
				'name': author.name,
				'account': author.student_id,
				'dateOfBirth': author.birth_date.strftime('%Y-%m-%d'),
				'major': author.major.name,
				'inYear': author.enroll_year,
				'fullNameOfwork': project.full_name,
				'postalAddress': author.contact_address,
				'phoneNumber': author.tel,
				'email': author.email,
				'currentEducation': author.education
			}
			partner = []
			co_authors = CoAuthor.objects.filter(project=project)
			for co_author in co_authors:
				tem_info = {
					'nameOfPartner': co_author.name,
					'studentIDOfPartner': co_author.student_id,
					'phoneOfPartner': co_author.tel,
					'emailOfPartner': co_author.email,
					'currenteducationOfPartner': co_author.education
				}
				partner.append(tem_info)
			tem['partner'] = partner
			data.append(tem)
		resp['competitionName'] = competition.name
		resp['data'] = data
		return HttpResponse(json.dumps(resp), content_type='application/json')
	if request.method == 'POST':
		# if at least one competition
		try:
			competition = Competition.objects.order_by('-start')[0]
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')
		# if student exist
		student_id = request.GET.get('studentID')
		try:
			student = Student.objects.get(student_id=student_id)
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')
		body = json.loads(request.body)
		# add author info
		setProjectAuthorInfo(student, body)
		# add project info
		project = Project()
		setProjectInfo(project, body, student, competition)
		# add coauthor info
		setProjectCoAuthorInfo(project, body)
		# if project submit
		if body['status'] != '未提交':
			formal_project = FormalProject()
			formal_project.project = project
			formal_project.save()
		return HttpResponse(json.dumps({'status': True}), content_type='application/json')
	if request.method == 'PUT':
		# if at least one competition
		try:
			competition = Competition.objects.order_by('-start')[0]
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')
		# if project exist
		try:
			project = Project.objects.get(pk=request.GET.get('id'))
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')
		body = json.loads(request.body)
		student = project.author
		setProjectAuthorInfo(student, body)
		setProjectInfo(project, body, student, competition)
		# remove all coauthor first
		co_authors = CoAuthor.objects.filter(project=project)
		for co_author in co_authors:
			co_author.delete()
		# add coauthor
		setProjectCoAuthorInfo(project, body)
		# if project submit
		if body['status'] != '未提交':
			formal_project = FormalProject()
			formal_project.project = project
			formal_project.save()
		return HttpResponse(json.dumps({'status': True}), content_type='application/json')

def setProjectAuthorInfo(student, body):
	birth_date = datetime.strptime(body['dateOfBirth'],'%Y-%m-%d')
	student.birth_date = birth_date
	student.contact_address = body['postalAddress']
	student.education = body['currentEducation']
	student.save()

def setProjectInfo(project, body, student, competition):
	project.name = body['nameOfWork']
	project.full_name = body['fullNameOfwork']
	project.competition = competition
	project.author = student
	project.project_type = body['classificationOfWork']
	project.category = body['declarationOfWork']
	project.description = body['overallDescriptionOfWork']
	project.innovation = body['innovationPoint']
	project.keyword = body['keyWord']
	project.status = body['status']
	project.save()

def setProjectCoAuthorInfo(project, body):
	co_authors = body['partner']
	for co_author in co_authors:
		if co_author['nameOfPartner'] != '':
			partner = CoAuthor()
			partner.student_id = co_author['studentIDOfPartner']
			partner.name = co_author['nameOfPartner']
			partner.tel = co_author['phoneOfPartner']
			partner.email = co_author['emailOfPartner']
			partner.education = co_author['currenteducationOfPartner']
			partner.project = project
			partner.save()

def student(request):
	if request.method == 'GET':
		student_id = request.GET.get('studentID')
		try:
			student = Student.objects.get(student_id=student_id)
			resp = {
				'account': student_id,
				'name': student.name,
				'department': student.school.name,
				'major': student.major.name,
				'inYear': student.enroll_year,
				'phoneNumber': student.tel,
				'email': student.email
			}
			return HttpResponse(json.dumps(resp), content_type='application/json')
		except:
			return HttpResponse(json.dumps({}), content_type='application/json')

def competition(request):
	if request.method == 'GET':
		competitions = Competition.objects.all()
		competition_list = []
		for competition in competitions:
			data = {
				'id': competition.id,
				'competitionName': competition.name,
				'acronym': competition.acronym,
				'startDate': competition.start.strftime('%Y-%m-%d'),
				'pre_review': competition.pre_review.strftime('%Y-%m-%d'),
				'checkDDL': competition.review.strftime('%Y-%m-%d'),
				'reviewDDL': competition.oral_defense.strftime('%Y-%m-%d'),
				'endDate': competition.end.strftime('%Y-%m-%d'),
				'description': competition.description
			}
			competition_list.append(data)
		return HttpResponse(json.dumps(competition_list), content_type='application/json')
	if request.method == 'POST':
		try:
			body = json.loads(request.body)
			competition = Competition()
			competition.name = body['competitionName']
			competition.acronym = body['acronym']
			competition.start = datetime.strptime(body['startDate'], '%Y-%m-%d')
			competition.pre_review = datetime.strptime(body['reviewDDL'], '%Y-%m-%d')
			competition.review = datetime.strptime(body['checkDDL'], '%Y-%m-%d')
			competition.oral_defense = datetime.strptime(body['checkDDL'], '%Y-%m-%d')
			competition.end = datetime.strptime(body['endDate'], '%Y-%m-%d')
			competition.description = body['description']
			competition.save()
			return HttpResponse(json.dumps({'status': True}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')

def test(request):
	if request.method == 'POST':
		try:
			tem_file = request.FILES.get('file')
			p = Project.objects.all()[0]
			p.video = tem_file
			p.save()
			return HttpResponse(json.dumps({'code': True, 'name': tem_file.name}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'code': False}), content_type='application/json')
