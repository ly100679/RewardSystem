import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rewardSystem.rewardSystem.settings'
from django.core.mail import EmailMultiAlternatives
from rewardSystem.rewardSystem.settings import PROJECTDIR
import xlrd


def sendMail(expert_name, expert_email):
	print(expert_name)
	print(expert_email)
	msg = EmailMultiAlternatives(
		'测试邮件',
		'''
		%s，你好。<br>
		是否要参加本届的评审？<br>
		233333333333333333!
		<br>
		接受评审请点击以下链接或复制到浏览器打开<br>
		<a href="#">test</a><br>
		拒绝评审请点击以下链接<br>
		<a href="#">23333</a>
		''' % expert_name,
		'2086607502@qq.com',
		[expert_email],
	)
	msg.content_subtype = 'html'
	try:
		msg.send()
		print('send %s email success' % expert_name)
	except:
		print('send %s email fail' % expert_name)

if __name__ == '__main__':
	with open('rewardSystem/tem_files/sendEmailToExpert', 'r+') as sendMailInfo:
		if_send_mail = sendMailInfo.read()
		print(if_send_mail)
		if if_send_mail != '1':
			if_send_mail = '1'
		elif if_send_mail != '0':
			if_send_mail = '0'
		sendMailInfo.seek(0)
		sendMailInfo.truncate()
		sendMailInfo.write(if_send_mail)
	if if_send_mail == '0':
		full_path = PROJECTDIR + 'tem_files/info.xlsx'
		data = xlrd.open_workbook(full_path)
		table = data.sheets()[0]
		expert_data = []
		# print(table.row_values(1)[0])
		for i in range(table.nrows):
			# expert_data.append({
			# 	'name': table.row_values(i)[0],
			# 	'account': table.row_values(i)[1],
			# 	'yield': table.row_values(i)[2]
			# })
			sendMail(str(table.row_values(i)[0]), str(table.row_values(i)[1]))
		
		# print(expert_data)
	