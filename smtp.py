import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_host = 'smtp.gmail.com'
smtp_port = 587
sender_email = "nurlanuuulubeksultan@gmail.com"
sender_password = "jaykglxvuuxalqnp"

receiver_email = "xxrxwoha@gmail.com"
subject = "Привет это текстовое сообщение!"

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

body = 'Тест'
message.attach(MIMEText(body, "plain"))

def send_email():
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Успешно отправлена")
    except Exception as e:
        print("Ошибка", e)
    finally:
        server.quit()

for _ in range(10):
    send_email()