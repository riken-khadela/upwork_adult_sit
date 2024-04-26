from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from main.models import sender_mail
import smtplib

def SendAnEmail(body: str, email=[], attachments=[]):
    obj = sender_mail.objects.first()
    if not obj : return
    sender_email = obj.email
    sender_password = obj.sender_password
    # receiver_email = "rikenkhadela777@gmail.com"  # Replace with the recipient's email address
    subject = obj.subject
    # sender_email = "demo@demo.sajaltech.com"
    # sender_password = "sajaltech"
    # receiver_email = "rikenkhadela777@gmail.com"  # Replace with the recipient's email address
    # subject = "Email Of an Error from webscrapping"
    body = f"""Hello, this is an email from Webscrapping server!\n
            An error we got : {body}
            Thanks.
            """

    if type(email)==list:
        for mail in email:
            # Construct the email message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = mail
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            for attachment in attachments:
                with open(attachment, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-Disposition", "attachment", filename=attachment)
                    message.attach(img)

            # Establish a connection with the SMTP server and send the email
            try:
                # with smtplib.SMTP_SSL(obj.server, obj.port) as server:
                with smtplib.SMTP_SSL("mail.demo.sajaltech.com", 465) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, mail, message.as_string())
                print(f"Email sent successfully!\nBody : {body}")
            except Exception as e:
                print(f"Error: {e}")
