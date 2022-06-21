import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(r_addr, content, subject='python'):
    # 邮件内容配置
    # 邮件文本
    msg = MIMEText(content, "html", "utf-8")
    # 邮件上显示的发件人
    msg["From"] = formataddr(["wx_python", "iiweixiao@yeah.net"])
    # 邮件上显示的主题
    msg["Subject"] = subject

    # 发送邮件
    server = smtplib.SMTP_SSL("smtp.yeah.net")
    server.login("iiweixiao@yeah.net", "IHHLUMDULZIKQPQR")  # "发件人的邮箱", "这里填写授权码"
    server.sendmail("iiweixiao@yeah.net", r_addr, msg.as_string())  # "发件人邮箱", "接受人邮箱"
    server.quit()
    # send_email(r_addr, content)


if __name__ == '__main__':
    content = '大家好，我是python机器人，\n现在测试一下'
    send_email("813703110@qq.com", content, 'test')
    # send_email("接收人2的邮箱")
    # send_email("接收人3的邮箱")
