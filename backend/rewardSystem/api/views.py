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
from . import sendMail
import zipfile
import numpy
import hashlib

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
			resp['canEdit'] = True if user.status == '0' else False
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
		competition = Competition.objects.filter(status__in=['作品提交', '团委初审', '专家评审', '现场答辩', '奖项公布'])[0]
	except:
		competition = None
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
			# committee required project status
			project_status = ['获奖', '未获奖', '现场答辩', '进入答辩', '未进入答辩', '评审中', '初审通过', '初审未通过', '初审中', '已提交']
			for status in project_status:
				current_status_project = Project.objects.filter(competition=competition, status=status)
				for tem in current_status_project:
					projects.append(tem)
		elif expert_id is not None:
			try:
				expert = Expert.objects.get(username=expert_id)
			except:
				return HttpResponse(json.dumps({'error': 'expert not found'}), content_type='application/json')
			projects = Project.objects.filter(expert=expert, competition=competition)
		elif student_id is not None:
			try:
				student = Student.objects.get(student_id=student_id)
			except:
				return HttpResponse(json.dumps({'error': 'student not found'}), content_type='application/json')
			project_status = ['获奖', '未获奖', '现场答辩', '进入答辩', '未进入答辩', '评审中', '初审通过', '初审未通过', '初审中', '已提交', '未提交']
			for status in project_status:
				current_status_project = Project.objects.filter(competition=competition, status=status, author=student)
				for tem in current_status_project:
					projects.append(tem)
		else:
			return HttpResponse(json.dumps({'error': 'unexpected request url'}), content_type='application/json')
		resp = {}
		data = []
		for project in projects:
			author = project.author # asdfasdf
			opinions = Opinion.objects.filter(project=project)
			total_score = 0
			i = 0
			for opinion in opinions:
				if opinion.expert.status == '0':
					continue
				try:
					tem_score = float(opinion.score)
					total_score = total_score + tem_score
					i = i + 1
				except:
					pass
			try:
				total_score = float(total_score) / i
			except:
				total_score = ''
			tem = {
				'id': project.id,
				'projectName': project.name,
				'projectID': getProjectID(project),
				'projectPeriod': project.status,
				'nameOfWork': project.name,
				'avgGrade': total_score,
				'classificationOfWork': project.project_type,
				'declarationOfWork': project.category,
				'overallDescriptionOfWork': project.description,
				'innovationPoint': project.innovation,
				'keyWord': project.keyword,
				'display': project.display,
				'research': project.research,
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
			if expert_id is not None:
				opinion = Opinion.objects.filter(expert=expert, project=project)
				tem['hasEdit'] = True if opinion.status != '0' else False
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
	birth_date = datetime.strptime(body['dateOfBirth'], '%Y-%m-%d')
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
	project.display = json.dumps(body['display'])
	project.research = json.dumps(body['research'])
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

def changeProjectStatus(competition, before_status, after_status):
	projects = Project.objects.filter(competition=competition, status=before_status)
	for project in projects:
		project.status = after_status
		project.save()

def setCompetition(competition, body):
	competition.name = body.get('competitionName', competition.name)
	competition.acronym = body.get('acronym', competition.acronym)
	competition.start = body.get('startDate', competition.start)
	competition.pre_review = body.get('submitDDL', competition.pre_review)
	competition.review = body.get('checkDDL', competition.review)
	competition.oral_defense = body.get('reviewDDL', competition.oral_defense)
	competition.end = body.get('endDate', competition.end)
	competition.description = body.get('description', competition.description)
	# reset expertlist when start a competition
	if competition.status == '未开始' and body.get('status', None) == '作品提交':
		expert_list = ExpertList.objects.all()
		for expert in expert_list:
			expert.status = '0'
			expert.save()
	# change project status when competiton status changed
	if competition.status == '作品提交' and body.get('status', None) == '团委初审':
		changeProjectStatus(competition, '已提交', '初审中')
	elif competition.status == '团委初审' and body.get('status', None) == '专家评审':
		changeProjectStatus(competition, '初审通过', '评审中')
		# send invite email to expert in list
		expert_list = ExpertList.objects.filter(status=0)
		expert_info_list = []
		for expert in expert_list:
			md5 = hashlib.md5()
			md5.update(str(expert.id).encode())
			expert.status = md5.hexdigest()
			expert_info_list.append({
				'name': expert.name,
				'email': expert.email,
				'field': expert.field,
				'code': expert.status
			})
			expert.save()
		project_info_list = {
			'A': [],
			'B': [],
			'C': [],
			'D': [],
			'E': [],
			'F': []
		}
		resp = {
			'expert_list': expert_info_list,
			'project_list': project_info_list
		}
		project_list = Project.objects.filter(competition=competition, status='评审中')
		for project in project_list:
			project_info_list[project.category].append({
				'name': project.name
			})
			# project_info_list['F'].append({
			# 	'name': project.name
			# })
		resp = json.dumps(resp)
		with open('tem_files/sendEmailToExpert', 'r+') as sendMailInfo:
			sendMailInfo.seek(0)
			sendMailInfo.truncate()
			sendMailInfo.write(resp)
	elif competition.status == '专家评审' and body.get('status', None) == '现场答辩':
		changeProjectStatus(competition, '进入答辩', '现场答辩')
	competition.status = body.get('status', competition.status)
	competition.save()

def competition(request):
	if request.method == 'GET':
		competition_id = request.GET.get('id', None)
		if competition_id is not None:
			competitions = [Competition.objects.get(pk=int(competition_id))]
		else:
			competitions = Competition.objects.all()
		competition_list = []
		for competition in competitions:
			data = {
				'id': competition.id,
				'competitionName': competition.name,
				'acronym': competition.acronym,
				'startDate': competition.start,
				'submitDDL': competition.pre_review,
				'checkDDL': competition.review,
				'reviewDDL': competition.oral_defense,
				'endDate': competition.end,
				'description': competition.description,
				'competitionStatus': competition.status
			}
			data['files'] = []
			competition_files = CompetitionFile.objects.filter(competition=competition)
			for competition_file in competition_files:
				data['files'].append(getFileInfoJson(competition_file.competition_file.name, 0))
			competition_list.append(data)
		if competition_id is not None:
			return HttpResponse(json.dumps(competition_list[0]), content_type='application/json')
		else:
			return HttpResponse(json.dumps({'data': competition_list}), content_type='application/json')
	if request.method == 'POST':
		# try:
		body = json.loads(request.body)
		competition = Competition()
		setCompetition(competition, body)
		return HttpResponse(json.dumps({'status': True}), content_type='application/json')
		# except:
		# 	return HttpResponse(json.dumps({'status': False}), content_type='application/json')
	if request.method == 'PUT':
		body = json.loads(request.body)
		competition = Competition.objects.get(pk=request.GET.get('id'))
		# ensure only one ongoing competition
		try:
			ongoing_competition = Competition.objects.filter(status__in=['作品提交', '团委初审', '专家评审', '现场答辩', '奖项公布'])[0]
			if body.get('status', None) in ['作品提交', '团委初审', '专家评审', '现场答辩', '奖项公布']:
				if competition.id != ongoing_competition.id:
					return HttpResponse(json.dumps({'status': False, 'error': 'already has an ongoing competition'}), content_type='application/json')
		except:
			pass
		setCompetition(competition, body)
		return HttpResponse(json.dumps({'status': True}), content_type='application/json')

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

def getSubmitFile(project):
	author = project.author
	data = {}
	display_types_dict = {}
	if project.project_type == str(0):
		s = 'invention_form.docx'
		tem_test = project.display
		display = json.loads(tem_test)
		for i in range(8):
			display_types_dict['isSomething'+str(i)] = '\u2611' if display[i] else '\u25a1'
	elif project.project_type == str(1):
		s = 'report_form.docx'
		research = json.loads(project.research)
		for i in range(15):
			display_types_dict['isSomething'+str(i)] = '\u2611' if research[i] else '\u25a1'
	else:
		s = "form.docx"
	document=MailMerge(s)
	# print(document.get_merge_fields())
	coauthors = CoAuthor.objects.filter(project=project)
	i = 0
	edu_dict = {
		'0': 'A',
		'1': 'B',
		'2': 'C',
		'3': 'D'
	}
	for coauthor in coauthors:
		i = i + 1
		data['name'+str(i)] = coauthor.name
		data['acc'+str(i)] = coauthor.student_id
		data['edu'+str(i)] = edu_dict[coauthor.education]
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
		data['isInvention'] = '\u2611'
		data['isReport'] = '\u25a1'
	else:
		data['isInvention'] = '\u25a1'
		data['isReport'] = '\u2611'
	# return HttpResponse(json.dumps({'path': project.full_name}), content_type='application/json')
	document.merge(
		projectID=getProjectID(project),
		workName=project.name,
		department=author.school.name,
		name=author.name,
		account=str(author.student_id),
		dateOfBirth=author.birth_date.strftime('%Y-%m-%d'),
		overalDescriptionOfWork=project.description,
		innovationPoint=project.innovation,
		keyword=project.keyword,
		major=author.major.name,
		inYear=str(author.enroll_year),
		fullNameOfWork=project.full_name,
		fullNameOfWork1=project.full_name,
		cat=project.category,
		postalAddress=author.contact_address,
		phoneNumber=author.tel,
		email=author.email,
		currentEducation=edu_dict[author.education],
		**data,
		**display_types_dict
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
	return form_path

def submitfile(request):
	project_id = request.GET.get('projectID')
	project = Project.objects.get(pk=project_id)
	form_path = getSubmitFile(project)
	return HttpResponse(json.dumps({'path': form_path}), content_type='application/json')

def expertProjectGrade(request):
	project_id = request.GET.get('id')
	expert_id = request.GET.get('expertID')
	try:
		project = Project.objects.get(pk=int(project_id))
		expert = Expert.objects.get(username=expert_id)
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
		try:
			opinion.score = float(body['grade'])
		except:
			opinion.score = 0
		opinion.opinion = body['advise']
		opinion.status = '1'
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
		i = 0
		grades = []
		for opinion in opinions:
			if opinion.expert.status == '0':
				continue
			try:
				tem_score = float(opinion.score)
				total_score = total_score + tem_score
				i = i + 1
			except:
				pass
			grades.append({
				'name': opinion.expert.name,
				'grade': opinion.score,
				'advise': opinion.opinion
			})
		try:
			total_score = float(total_score) / i
		except:
			total_score = ''
		resp = {
			'avgGrade': total_score,
			'grades': grades
		}
		return HttpResponse(json.dumps(resp), content_type='application/json')

def expertList(request):
	if request.method == 'POST':
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
			for i in range(table.nrows):
				try:
					tem = ExpertList.objects.get(email=table.row_values(i)[1])
				except:
					tem = ExpertList()
					tem.name = table.row_values(i)[0]
					tem.email = table.row_values(i)[1]
					tem.field = table.row_values(i)[2]
					tem.save()
			return HttpResponse(json.dumps(expert_data), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'code': False}), content_type='application/json')
	if request.method == 'GET':
		expert_list = ExpertList.objects.all()
		resp = []
		for expert in expert_list:
			resp.append({
				'name': expert.name,
				'account': expert.email,
				'yield': expert.field
			})
		return HttpResponse(json.dumps(resp), content_type='application/json')

def expert(request):
	if request.method == 'GET':
		try:
			competition = Competition.objects.filter(status__in=['作品提交', '团委初审', '专家评审'])[0]
		except:
			return HttpResponse(json.dumps({'error': 'competition number is 0'}), content_type='application/json')
		expert_username = request.GET.get('email')
		expert_code = request.GET.get('code')
		try:
			expert_info = ExpertList.objects.get(status=expert_code)
		except:
			return HttpResponse(json.dumps({'error': 'no such code'}), content_type='application/json')
		try:
			expert = Expert.objects.get(username=expert_info.email)
		except:
			expert = Expert.objects.create_user(expert_info.email, expert_info.email, '123456')
			expert.name = expert_info.name
			expert.field = expert_info.field
			expert.save()
		projects = Project.objects.filter(competition=competition, category=expert.field, status='评审中')
		for project in projects:
			try:
				opinion = Opinion.objects.get(expert=expert, project=project)
			except:
				opinion = Opinion()
				opinion.expert = expert
				opinion.project = project
				opinion.save()
		sendMail.sendExpertAccountEmail(expert.name, expert.username)
		return HttpResponse('success! You will recieve an email contains your account info shortly')
	if request.method == 'PUT':
		expert_id = request.GET.get('expertID')
		expert = Expert.objects.get(username=expert_id)
		expert.status = '1'
		expert.save()
		return HttpResponse(json.dumps({'status': True}), content_type='application/json')

def zipProject(request):
	expert_id = request.GET.get('expertID')
	body = json.loads(request.body)
	project_ids = body['id']
	zip_file_name = 'tem_files/%s.zip' % expert_id
	z = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
	print(os.sep)
	resp = []
	# handle submit file
	try:
		for project_id in project_ids:
			project = Project.objects.get(pk=project_id)
			getSubmitFile(project)
	except:
		return HttpResponse(json.dumps({'filepath': 'project not exist'}), content_type='application/json')
	for dirpath, dirnames, filenames in os.walk('submit_file'):
		for filename in filenames:
			if filename == '.gitkeep':
				continue
			try:
				project_id = re.sub('form1.docx', '', filename)
				project_id = int(project_id)
			except:
				continue
			# if project id in request id list, zip this file
			if int(project_id) in project_ids:
				z.write(dirpath+os.sep+filename, str(project_id) + os.sep + 'form.docx')
	getZipProject('project_file', expert_id, z, project_ids)
	getZipProject('project_img', expert_id, z, project_ids)
	getZipProject('project_video', expert_id, z, project_ids)
	z.close()
	return HttpResponse(json.dumps({'filepath': zip_file_name}), content_type='application/json')

def getZipProject(folder_name, expert_id, z, project_ids):
	for dirpath, dirnames, filenames in os.walk(folder_name):
		zip_file_path = dirpath
		for filename in filenames:
			if filename == '.gitkeep':
				continue
			project_id = re.match(r'proj([0-9]*?)name', filename).group(1)
			formal_filename = re.sub('proj\S*?name', '', filename)
			# if project id in request id list, zip this file
			if int(project_id) in project_ids:
				z.write(dirpath+os.sep+filename, str(project_id) + os.sep + folder_name + os.sep + formal_filename)

def currenCompetition(request):
	try:
		competition = Competition.objects.filter(status__in=['作品提交', '团委初审', '专家评审', '现场答辩', '奖项公布'])[0]
	except:
		return HttpResponse(json.dumps({'error': 'competition number is 0'}), content_type='application/json')
	data = {
		'id': competition.id,
		'competitionName': competition.name,
		'acronym': competition.acronym,
		'startDate': competition.start,
		'submitDDL': competition.pre_review,
		'checkDDL': competition.review,
		'reviewDDL': competition.oral_defense,
		'endDate': competition.end,
		'description': competition.description,
		'competitionStatus': competition.status
	}
	data['files'] = []
	competition_files = CompetitionFile.objects.filter(competition=competition)
	for competition_file in competition_files:
		data['files'].append(getFileInfoJson(competition_file.competition_file.name, 0))
	return HttpResponse(json.dumps(data), content_type='application/json')
