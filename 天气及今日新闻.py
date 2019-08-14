'''
爬取新闻，及每日天气，通过邮件发送到QQ
'''
'''
from socket import socket
import ssl
import re
sock = ssl.wrap_socket(socket())
ser_addr = ('www.toutiao.com', 443)
sock.connect(ser_addr)
req = 'GET /ch/news_hot/ HTTP/1.1\r\nConnection: close\r\nHost: www.toutiao.com\r\n\r\n'
sock.send(req.encode())
data = b''
while True:
    recv_data = sock.recv(512)
    if recv_data:
        data += recv_data
    else:
        break
# data = data.decode(encoding="unicode-escape", errors='ignore')
data = data.decode()
r = re.findall('\"group_id\":\"\d{19}\"', data)

for x in r:
    str_1 = 'www.toutiao.com'+'/a'+x[x.find(':')+1:].replace('"','')
    print(str_1)

sock.close()
'''

# 导入模块
from socket import socket  # 套接字模块
# HTTPS模块
import ssl
# 正则表达式模块
import re
# 邮件模块
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 发送邮箱
def send_email(data):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "2115056561@qq.com"  # 用户名
    mail_pass = "jwcbxdwayhoeeajg"  # 口令

    sender = '2115056561@qq.com'
    receivers = ['2115056561@qq.com', ]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 发送内容
    message = MIMEText(data, 'plain', 'utf-8')
    # 发件人
    message['From'] = Header("吕浩亮", 'utf-8')
    # 收件人
    message['To'] = Header("LHL", 'utf-8')

    # 发送标题
    subject = '今日头条即天气'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)  # SMTP over SSL 默认端口号为465
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

# 连接服务器，获取服务器返回的消息
def s_r(ser, UIL, port):
    sock = ssl.wrap_socket(socket())
    # ser_addr = ('www.toutiao.com', 443)
    ser_addr = (ser, port)
    sock.connect(ser_addr)
    req = 'GET /%s HTTP/1.1\r\nConnection: close\r\nHost: %s\r\n\r\n' % (UIL, ser)
    sock.send(req.encode())
    data = b''
    while True:
        recv_data = sock.recv(512)
        if recv_data:
            data += recv_data
        else:
            break
    # print(data)
    sock.close()
    return data.decode(errors='ignore')

# 内容存放路径
file_path = 'C:\\Users\Administrator\Desktop\z\\新闻及天气.txt'

'''
每日新闻
'''
data = s_r('www.toutiao.com', 'ch/news_hot/', 443)
r = re.findall('\"group_id\":\"\d{19}\"', data)
f = open(file_path, 'wb')
for x in r:
    str_1 = 'www.toutiao.com'+'/a'+x[x.find(':')+1:].replace('"', '')
    str_2 = 'a'+x[x.find(':')+1:].replace('"', '')
    data = s_r('www.toutiao.com', str_2, 443)   # str
    if re.search('<title>(.+?)</title>', data):
        data = re.search('<title>(.+?)</title>', data).group().replace('<title>', '').replace('</title>', '')
        data = str_1 + ' :' + data + '\r\n'
        f.write(data.encode())
        #print(data)

'''
每日天气
'''
data = s_r('www.tianqi.com', 'wuhan/', 443)
# 城市
str_1 = re.search('<dd class=\"name\"><h2>(.+?)</h2>', data).group()
str_1 = str_1[str_1.find('<h2>')+len('<h2>'):str_1.find('</h2>')]
# 日期
str_2 = re.search('<dd class="week">(.+?)</dd>', data).group()
str_2 = str_2[len('<dd class="week">'):str_2.find('</dd>')]
# 天气及温度
str_3 = re.search('<span>(.+?)</span>', data).group()
str_3 = str_3[len('<span><b>'):str_3.find('</b>')] + ':' + str_3[str_3.find('</b>')+len('</b>'):str_3.find('</span>')]
data = str_1 + '\r\n' + str_2 + '\r\n' + str_3
f.write(data.encode())
#print(data)
f.close()

'''
发送邮件
'''
with open(file_path, 'rb') as f:
    data = f.read().decode()
# 发送邮件
send_email(data)


