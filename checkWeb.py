import os
import requests
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(subject, html_body, to_email, attachment_path=None):
    from_email = "yourmail"
    password = "yourpassword"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_body, 'html'))  # 将邮件正文添加为 HTML 格式
    # msg.attach(MIMEText(body, 'plain'))


    if attachment_path:
        for attachment_path_temp in attachment_path:
            attachment = open(attachment_path_temp, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path_temp)}')

            msg.attach(part)

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def check_website(url,email):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"Website {url} is up and running.")
        else:
            print(f"Website {url} returned status code {response.status_code}.")
            send_email("Website Alert", f"Website {url} returned status code {response.status_code}.", f"{email}")
        return 3600
    except Exception as e:
        print(f"Website {url} is down. Error: {e}")
        return 5

if __name__ == "__main__":
    url_to_check = "https://yoursite/"
    timeD = 5
    time1 = time.time()
    while True:
        if timeD==3600:time1 = time.time()
        timeD = check_website(url_to_check,"yourmail")
        if timeD!=3600:
            time2 = time.time()
            print(f"Time used: {time2 - time1} seconds.")
        time.sleep(timeD)  # 3600休眠一小時
