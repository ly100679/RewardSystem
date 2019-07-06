import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rewardSystem.rewardSystem.settings'
from django.core.mail import EmailMultiAlternatives
from rewardSystem.rewardSystem.settings import PROJECTDIR
import xlrd
import json
import time
import platform


def sendMail(expert, expert_email, project_list):
	print(expert_email)
	email_project_str = ''
	for project in project_list:
		email_project_str = email_project_str + project['name'] + '<br>'
	accept_url = '180.76.111.16/expert?email=%s&code=%s' % (expert_email, expert['code'])
	msg = EmailMultiAlternatives(
		'测试邮件',
		'''
		%s，你好。<br>
		是否要参加本届的评审？<br>
		需要评审的参赛作品如下：<br>
		%s
		<br>
		接受评审请点击以下链接或复制到浏览器打开<br>
		<a href="%s">%s</a><br>
		''' % (expert['name'], email_project_str, accept_url, accept_url),
		'2086607502@qq.com',
		[expert_email],
	)
	msg.content_subtype = 'html'
	try:
		msg.send()
		print('send %s email success' % expert['name'])
	except:
		print('send %s email fail' % expert['name'])

if __name__ == '__main__':
	if platform.system() == 'Windows':
    	e_url = 'rewardSystem/tem_files/sendEmailToExpert'
	else:
    	e_url = '/root/RewardSystem/backend/rewardSystem/tem_files/sendEmailToExpert'
	while True:
		with open(e_url, 'r+') as sendMailInfo:
			if_send_mail = sendMailInfo.read()
			print(if_send_mail)
			if if_send_mail != '':
				data = json.loads(if_send_mail)
				expert_list = data['expert_list']
				project_list = data['project_list']
				for i in expert_list:
					sendMail(i, i['email'], project_list[i['field']])
				sendMailInfo.seek(0)
				sendMailInfo.truncate()
				sendMailInfo.write('')
			else:
				print('nothing to do')
		time.sleep(60)
		