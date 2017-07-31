#! python3
# coding:utf-8
import requests
import time
import os
import shutil
import smtplib
from email.header import Header
from email.mime.text import MIMEText

# 蒲公英key
u_key = 'c23784bcc4797236ecb6db5c012ef8c3'
api_key = '2fd28a7b0c3cd053d8fb1c4380472e8d'

# 获取当前日期
nowdate = time.strftime('%Y%m%d', time.localtime(time.time()))
# 上传文件
url = 'http://qiniu-storage.pgyer.com/apiv1/app/upload'
filename = 'GreenTownLife_' + nowdate + '.ipa'
filepath = './build/ipa/' + nowdate + '/' + filename
files = {'file': open(filepath, 'rb')}
data = {'uKey': u_key, '_api_key': api_key}
r = requests.post(url, data=data, files=files)

# 获取当前目录
current_path = os.path.split(os.path.realpath(__file__))[0]
# 删除文件夹
if r.status_code == 200:
    print('蒲公英上传成功！')
    rmdir = os.path.join(current_path, 'build')
    if os.path.isdir(rmdir):
        shutil.rmtree(rmdir, True)
        print('文件删除成功！')


def sendMail(targetMaillist):
    mailBody = '你好，应用下载地址：https://www.pgyer.com/wT0u'
    # 申明邮件对象
    msg = MIMEText(mailBody, 'html', 'utf-8')
    # 邮件主题
    msg['subject'] = Header('iOS 自动build', 'utf-8')
    msg['From'] = 'zhouyi<joey01265235@163.com>'

    # SMTP服务对象
    smtpMail = smtplib.SMTP()

    # 连接SMTP服务器
    smtpMail.connect('smtp.163.com')

    # 登录SMTP服务器
    smtpMail.login('joey01265235@163.com', 'zylovekll5051560')

    # 使用SMTP服务器发送邮件
    for tgmail in targetMaillist:
        msg['To'] = tgmail
        smtpMail.sendmail('joey01265235@163.com', tgmail, msg.as_string())
        print('** 邮件发送成功！ **')
    smtpMail.quit()


# 发送邮件
# 接收邮件列表
targetMaillist = ['joey01265235@163.com', '121903163@qq.com']
sendMail(targetMaillist)
