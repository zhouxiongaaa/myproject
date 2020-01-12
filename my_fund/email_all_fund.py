'''从MySQL提取基金数据，并作图发送到邮箱'''

import smtplib
import pymysql
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def get_fund_data_and_draw():
    global results1
    # 前期循环查询与绘图准备
    fig = plt.figure(figsize=(12, 12), dpi=120)
    fund_name_list = ['110022', '110003', '519732', '001938', '110011', '260108']
    results1 = ()
    local_list = [611, 612, 613, 614, 615, 616]
    for li, b in zip(fund_name_list, local_list):
        sql = 'SELECT fund_code, fund_price, date FROM fund_data where fund_code = "'+li+'"'
        try:
            cursor.execute(sql)
            r = cursor.fetchall()
            results1 += r
            print(results1)
        except:
            print("Error: unable to fetch data")
        x = []
        y = []
        for l in range(len(r)):
            x.append(r[l][2])
            y.append(r[l][1])
        # 配置横坐标
        ax = plt.gca()
        xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in x]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        ax.set_xticks(xs)

        ax = plt.subplot(b, facecolor='#A9A9A9')  # 定位位置
        plt.ylabel(u''+r[0][0]+'(¥)', fontsize='15', color='r')
        plt.xlabel(u'day', fontproperties='simhei', fontsize='20', color='r')
        plt.plot(xs, y, color="r", marker='o', markerfacecolor='blue', markersize=3)
        plt.gcf().autofmt_xdate()

    # 关闭数据库连接
    cursor.close()
    db.close()

    # 保存并出图
    fig.tight_layout()
    # plt.subplots_adjust(wspace=0, hspace=0) #调整子图间距
    plt.savefig("a.png")
    plt.show()


def send_email(results1):
    # 构造html+图片的邮件内容
    subject = '基金数据'
    msgRoot = MIMEMultipart('related')
    email_text = str(results1).replace('(', '').replace(')', '\n')
    print(email_text)
    msgText = MIMEText(email_text, 'html', 'utf-8')
    msgRoot.attach(msgText)

    fp = open('C:\\git project\\my_fund\\a.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '')
    msgRoot.attach(msgImage)

    receiver = '1315571709@qq.com'
    # receiver = '13476118967@139.com'
    sender = 'zhouxiong@whu.edu.cn'
    pwd = 'a4592948'
    # msg = MIMEText(results, 'html', 'utf-8')  # 发送html
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender  # 发送者
    msgRoot['To'] = receiver  # 接收者
    try:
        sentObj = smtplib.SMTP('smtp.whu.edu.cn', 25)
        sentObj.login(sender, pwd)
        sentObj.sendmail(sender, receiver, msgRoot.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "a4592948", "fund")
    cursor = db.cursor()
    get_fund_data_and_draw()
    send_email(results1)




