import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rewardSystem.rewardSystem.settings'
from django.core.mail import EmailMultiAlternatives


if __name__ == '__main__':
    msg = EmailMultiAlternatives(
        '测试邮件',
        '''
        XXXXX，你好。<br>
        是否要参加本届XXXXX的评审？<br>
        233333333333333333!
        <br>
        接受评审请点击以下链接或复制到浏览器打开<br>
        <a>test</a><br>
        拒绝评审请点击以下链接<br>
        <a>23333</a>
        ''',
        '2086607502@qq.com',
        ['2254106707@qq.com', 'carl710082796@hotmail.com'],
    )
    msg.content_subtype = 'html'
    msg.send()
    print(233)