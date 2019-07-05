from django.core.mail import EmailMultiAlternatives

def sendExpertAccountEmail(expert_name, expert_email):
	msg = EmailMultiAlternatives(
		'测试邮件',
		'''
		%s，你好。<br>
		你已参加本次评审<br>
		你的账号为：%s
		<br>
		如果这是你第一次使用系统，你的默认密码为：123456<br>
		你可前往<a>180.76.111.16</a>登录<br>
		''' % (expert_name, expert_email),
		'2086607502@qq.com',
		[expert_email],
	)
	msg.content_subtype = 'html'
	msg.send()