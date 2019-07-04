from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import *
import json
from datetime import datetime
from rewardSystem.settings import PROJECTDIR
import os
import re
from mailmerge import MailMerge
import platform
import xlrd

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
	# if at least one competition
	try:
		competition = Competition.objects.order_by('-start')[0]
	except:
		return HttpResponse(json.dumps({'error': 'competition number is 0'}), content_type='application/json')
	if request.method == 'GET':
		projects = []
		# if request has attr id
		project_id = request.GET.get('id', None)
		competition_id = request.GET.get('competitionID', None)
		expert_id = request.GET.get('expertID', None)
		student_id = request.GET.get('studentID', None)
		if project_id is not None:
			projects.append(Project.objects.get(pk=project_id))
		elif competition_id is not None:
			try:
				competition = Competition.objects.get(pk=competition_id)
			except:
				return HttpResponse(json.dumps({'error': 'competition not found'}), content_type='application/json')
			projects.append(Project.objects.filter(competition=competition))
		elif expert_id is not None:
			try:
				expert = Expert.objects.get(pk=competition_id)
			except:
				return HttpResponse(json.dumps({'error': 'expert not found'}), content_type='application/json')
			projects.append(Project.objects.filter(expert=expert, competition=competition))
		elif student_id is not None:
			try:
				student = Student.objects.get(student_id=student_id)
			except:
				return HttpResponse(json.dumps({'error': 'student not found'}), content_type='application/json')
			projects = Project.objects.filter(author=student, competition=competition)
		else:
			return HttpResponse(json.dumps({'error': 'unexpected request url'}), content_type='application/json')
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
			project_file_info = getProjectFile(project)
			tem['files'] = project_file_info['files']
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
		# body = json.loads(request.body)
		# # add author info
		# setProjectAuthorInfo(student, body)
		# # add project info
		# project = Project()
		# setProjectInfo(project, body, student, competition)
		# # add coauthor info
		# setProjectCoAuthorInfo(project, body)
		# return HttpResponse(json.dumps({'status': True, 'id':project.id}), content_type='application/json')
		project = Project()
		project.status = '未提交'
		project.save()
		return HttpResponse(json.dumps({'code': project.id}), content_type='application/json')
	if request.method == 'PUT':
		body = json.loads(request.body)
		# if project exist
		try:
			project = Project.objects.get(pk=request.GET.get('id'))
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')
		# if student exist
		# save project form
		# else just change project status
		student_id = request.GET.get('studentID')
		try:
			student = Student.objects.get(student_id=student_id)
			setProjectAuthorInfo(student, body)
			setProjectInfo(project, body, student, competition)
			# remove all coauthor first
			co_authors = CoAuthor.objects.filter(project=project)
			for co_author in co_authors:
				co_author.delete()
			# add coauthor
			setProjectCoAuthorInfo(project, body)
		except:
			project.status = body['status']
			project.save()
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

def getCompetitionStatus(competition):
	current_time = datetime.now()
	if competition.end < current_time:
		return 'end'
	elif competition.oral_defense < current_time:
		return 'oral_defense'
	elif competition.review < current_time:
		return 'review'
	elif competition.pre_review < current_time:
		return 'pre_review'
	elif competition.start < current_time:
		return 'start'
	else:
		return 'before start'

def competition(request):
	if request.method == 'GET':
		competition_id = request.GET.get('id', None)
		if competition_id is not None:
			competitions = Competition.objects.get(pk=int(competition_id))
		else:
			competitions = Competition.objects.all()
		competition_list = []
		for competition in competitions:
			data = {
				'id': competition.id,
				'competitionName': competition.name,
				'acronym': competition.acronym,
				'startDate': competition.start.strftime('%Y-%m-%d'),
				'submitDDL': competition.pre_review.strftime('%Y-%m-%d'),
				'checkDDL': competition.review.strftime('%Y-%m-%d'),
				'reviewDDL': competition.oral_defense.strftime('%Y-%m-%d'),
				'endDate': competition.end.strftime('%Y-%m-%d'),
				'description': competition.description,
				'competitionStatus': getCompetitionStatus(competition)
			}
			competition_list.append(data)
		if competition_id is not None:
			return HttpResponse(json.dumps(competition_list[0]), content_type='application/json')
		else:
			return HttpResponse(json.dumps({'data': competition_list}), content_type='application/json')
	if request.method == 'POST':
		try:
			body = json.loads(request.body)
			competition = Competition()
			competition.name = body['competitionName']
			competition.acronym = body['acronym']
			competition.start = datetime.strptime(body['startDate'], '%Y-%m-%d')
			competition.pre_review = datetime.strptime(body['submitDDL'], '%Y-%m-%d')
			competition.review = datetime.strptime(body['checkDDL'], '%Y-%m-%d')
			competition.oral_defense = datetime.strptime(body['reviewDDL'], '%Y-%m-%d')
			competition.end = datetime.strptime(body['endDate'], '%Y-%m-%d')
			competition.description = body['description']
			competition.save()
			return HttpResponse(json.dumps({'status': True}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'status': False}), content_type='application/json')

def competitionFile(request):
	competition_id = request.GET.get('competitionID', None)
	try:
		competition = Competition.objects.get(pk=competition_id)
	except:
		return HttpResponse(json.dumps({'error': 'competition not found'}), content_type='application/json')
	if request.method == 'GET':
		competition_files = CompetitionFile.objects.filter(competition=competition)
		resp = {
			'files': []
		}
		for competition_file in competition_files:
			resp['files'].append(getFileInfoJson(competition_file.competition_file.name, 0))
		return HttpResponse(json.dumps(resp), content_type='application/json')
	if request.method == 'POST':
		competition_file = request.FILES.get('file')
		competition_file.name = 'comp%sname%s' % (str(competition.id), competition_file.name)
		tem = CompetitionFile()
		tem.competition = competition
		tem.competition_file = competition_file
		tem.save()
		return HttpResponse(json.dumps({'code': True}), content_type='application/json')
	if request.method == 'DELETE':
		body = json.loads(request.body)
		file_name = body['filename']
		file_name = 'proje_competition_file/comp%sname%s' % (str(competition.id), file_name)
		competition_file = CompetitionFile.objects.get(competition=competition, competition_file=file_name)
		competition_file.delete()
		if not deleteFileFromFolder(file_name):
			return HttpResponse(json.dumps({'code': False, 'file_path': file_name}), content_type='application/json')
		return HttpResponse(json.dumps({'code': True, 'file_path': file_name}), content_type='application/json')

def deleteFileFromFolder(file_name):
	name = PROJECTDIR + file_name
	if os.path.exists(name):
		os.remove(name)
		return True
	else:
		return False

def getFileInfoJson(path, filetype):
	filename = re.sub('proje\S*?name', '', path)
	full_path = PROJECTDIR + path
	try:
		datasize = os.path.getsize(full_path)
		datasize = float(datasize) / 1024
	except:
		datasize = 0
	return {
		'filename': filename,
		'path': path,
		'type': filetype,
		'datasize': datasize
	}

def getProjectFile(project):
	resp = {
		'files': []
	}
	if project.video is not None:
		resp['files'].append(getFileInfoJson(project.video.name, 2))
	files = ProjectImg.objects.filter(project=project)
	for img in files:
		resp['files'].append(getFileInfoJson(img.img.name, 0))
	files = ProjectFile.objects.filter(project=project)
	for pfile in files:
		resp['files'].append(getFileInfoJson(pfile.pdf.name, 1))
	return resp

def projectFile(request):
	if request.method == 'POST':
		project_id = request.GET.get('projectID')
		file_type = int(request.GET.get('type'))
		try:
			project = Project.objects.get(pk=project_id)
			project_file = request.FILES.get('file')
			project_file.name = 'proj%sname%s' % (str(project.id), project_file.name)
			if file_type == 0:
				img = ProjectImg()
				img.project = project
				img.img = project_file
				img.save()
			elif file_type == 1:
				pfile = ProjectFile()
				pfile.project = project
				pfile.pdf = project_file
				pfile.save()
			elif file_type == 2:
				project.video = project_file
				project.save()
			return HttpResponse(json.dumps({'code': True}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'code': False}), content_type='application/json')
	if request.method == 'DELETE':
		try:
			file_type = int(request.GET.get('type'))
			prefix = 'project_img'
			if file_type == 1:
				prefix = 'project_file'
			elif file_type == 2:
				prefix = 'project_video'
			body = json.loads(request.body)
			file_name = body['filename']
			project_id = request.GET.get('projectID')
			project = Project.objects.get(pk=project_id)
			file_name = '%s/proj%sname%s' % (prefix, str(project.id), file_name)
			if file_type == 0:
				img = ProjectImg.objects.get(img=file_name)
				img.delete()
			elif file_type == 1:
				pfile = ProjectFile.objects.get(pdf=file_name)
				pfile.delete()
			elif file_type == 2:
				project.video = None
				project.save()
			# delete file from project folder
			if not deleteFileFromFolder(file_name):
				return HttpResponse(json.dumps({'code': False, 'file_full_path': file_name}), content_type='application/json')
			return HttpResponse(json.dumps({'code': True, 'file_full_path': file_name}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'code': False}), content_type='application/json')
	if request.method == 'GET':
		project = Project.objects.get(pk=int(request.GET.get('projectID')))
		resp = getProjectFile(project)
		return HttpResponse(json.dumps(resp), content_type='application/json')

def submitfile(request):
	project_id = request.GET.get('projectID')
	project = Project.objects.get(pk=project_id)
	author = project.author
	s = "form.docx"
	document=MailMerge(s)
	# print(document.get_merge_fields())
	data = {}
	coauthors = CoAuthor.objects.filter(project=project)
	i = 0
	for coauthor in coauthors:
		i = i + 1
		data['name'+str(i)] = coauthor.name
		data['acc'+str(i)] = coauthor.student_id
		if coauthor.education == '0':
			data['edu'+str(i)] = 'A'
		elif coauthor.education == '1':
			data['edu'+str(i)] = 'B'
		elif coauthor.education == '2':
			data['edu'+str(i)] = 'C'
		elif coauthor.education == '3':
			data['edu'+str(i)] = 'D'
		data['phoneno'+str(i)] = coauthor.tel
		data['email'+str(i)] = coauthor.email
	while i < 4:
		i = i + 1
		data['name'+str(i)] = ''
		data['acc'+str(i)] = ''
		data['edu'+str(i)] = ''
		data['phoneno'+str(i)] = ''
		data['email'+str(i)] = ''
	if project.project_type == '0':
		data['isInvention'] = u'✓'
		data['isReport'] = ''
	else:
		data['isInvention'] = ''
		data['isReport'] = u'✓'
	if author.education == '0':
		data['edu0'] = 'A'
	elif author.education == '1':
		data['edu0'] = 'B'
	elif author.education == '2':
		data['edu0'] = 'C'
	elif author.education == '3':
		data['edu0'] = 'D'
	document.merge(
		projectID=getProjectID(project),
		workName=project.name,
		department=author.school.name,
		isInvention=data['isInvention'],
		isReport=data['isReport'],
		name=author.name,
		account=str(author.student_id),
		dateOfBirth=author.birth_date.strftime('%Y-%m-%d'),
		overalDescriptionOfWork=project.description,
		innovationPoint=project.innovation,
		keyword=project.keyword,
		major=author.major.name,
		inYear=str(author.enroll_year),
		fullNameOfwork=project.full_name,
		fullNameOfwork1=project.full_name,
		cat=project.category,
		postalAddress=author.contact_address,
		phoneNumber=author.tel,
		email=author.email,
		currentEducation=data['edu0'],
		name1=data['name1'],
		name2=data['name2'],
		name3=data['name3'],
		name4=data['name4'],
		acc1=data['acc1'],
		acc2=data['acc2'],
		acc3=data['acc3'],
		acc4=data['acc4'],
		edu1=data['edu1'],
		edu2=data['edu2'],
		edu3=data['edu3'],
		edu4=data['edu4'],
		phoneno1=data['phoneno1'],
		phoneno2=data['phoneno2'],
		phoneno3=data['phoneno3'],
		phoneno4=data['phoneno4'],
		email1=data['email1'],
		email2=data['email2'],
		email3=data['email3'],
		email4=data['email4'],
	)
	form_path = 'submit_file/%sform1.docx' % str(project.id)
	form_full_path = PROJECTDIR + form_path
	if platform.system() == 'Windows':
		document.write(form_path)
	else:
		document.write(form_full_path)
	if platform.system() != 'Windows':
		ret = os.system('unoconv -f pdf --output=/root/RewardSystem/backend/rewardSystem/submit_file %s' % (form_full_path))
		form_path = 'submit_file/%sform1.pdf' % str(project.id)
	return HttpResponse(json.dumps({'path': form_path}), content_type='application/json')

def expertProjectGrade(request):
	project_id = request.GET.get('id')
	expert_id = request.GET.get('expertID')
	try:
		project = Project.objects.get(pk=int(project_id))
		expert = Expert.objects.get(pk=int(expert_id))
	except:
		return HttpResponse(json.dumps({'error': 'no such expert or project found'}), content_type='application/json')
	if request.method == 'POST':
		# get opinion if already exist
		# create opinion if not
		try:
			opinion = Opinion.objects.get(project=project, expert=expert)
		except:
			opinion = Opinion()
			opinion.project = project
			opinion.expert = expert
			opinion.save()
		body = json.loads(request.body)
		opinion.score = float(body['grade'])
		opinion.opinion = body['advise']
		opinion.save()
		return HttpResponse(json.dumps({'status': True}), content_type='application/json')
	if request.method == 'GET':
		try:
			opinion = Opinion.objects.get(project=project, expert=expert)
		except:
			return HttpResponse(json.dumps({'error': 'opinion not found'}), content_type='application/json')
		resp = {
			'grade': opinion.score,
			'advise': opinion.opinion
		}
		return HttpResponse(json.dumps(resp), content_type='application/json')

def schoolProjectGrade(request):
	if request.method == 'GET':
		project = Project.objects.get(pk=int(request.GET.get('id')))
		opinions = Opinion.objects.filter(project=project)
		total_score = 0
		grades = []
		for opinion in opinions:
			total_score = total_score + opinion.score
			grades.append({
				'name': opinion.expert.name,
				'grade': opinion.score,
				'advise': opinion.opinion
			})
		total_score = total_score / len(opinions)
		resp = {
			'avgGrade': total_score,
			'grades': grades
		}
		return HttpResponse(json.dumps(resp), content_type='application/json')

def expertList(request):
	try:
		expert_list_file = request.FILES.get('file')
		full_path = PROJECTDIR + 'tem_files/info.xlsx'
		with open(full_path, 'wb+') as f:
			for chunk in expert_list_file.chunks():
				f.write(chunk)
		f.close()
		data = xlrd.open_workbook(full_path)
		table = data.sheets()[0]
		expert_data = []
		for i in range(table.nrows):
			expert_data.append({
				'name': table.row_values(i)[0],
				'account': table.row_values(i)[1],
				'yield': table.row_values(i)[2]
			})
		# if at least one competition
		try:
			competition = Competition.objects.order_by('-start')[0]
		except:
			return HttpResponse(json.dumps({'error': 'competition number is 0'}), content_type='application/json')
		for i in range(table.nrows):
			try:
				tem = ExpertList.objects.get(email=table.row_values(i)[1])
			except:
				tem = ExpertList()
				tem.competition = competition
				tem.name = table.row_values(i)[0]
				tem.email = table.row_values(i)[1]
				tem.field = table.row_values(i)[2]
				tem.save()
		# send invite email
		expert_list = ExpertList.objects.filter(status=0)

		return HttpResponse(json.dumps(expert_data), content_type='application/json')
	except:
		return HttpResponse(json.dumps({'code': False}), content_type='application/json')
