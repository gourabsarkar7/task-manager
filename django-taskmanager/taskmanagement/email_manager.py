"""Email Manager for this app"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from multiprocessing import AuthenticationError
import smtplib
from jinja2 import Environment

from email.message import EmailMessage
from rest_framework import status
from response import Response as ResponseData
from requests import Response
from projects.models import ProjectAssigneeModel
from taskmanagement.config import Config  # Jinja2 templating

CHARSET = "UTF-8"
SENDER_EMAIL = Config.SENDER_EMAIL
port  = 25
password = "Radixweb@13"
smtp_server = "192.168.100.101"
SENDER_EMAIL="anirudh.chawla@radixweb.com"

class EmailManager:
    """Class for managing email"""

    def send_email(self, recipient, subject, project_id, assignee_id,template):
        """Function for sending email"""
        try:
            message = EmailMessage()
            message.add_alternative(Environment().from_string(template).render(
                    title='Hello World!'
                ))
            # message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            s = smtplib.SMTP('localhost')
            s.send_message(message)
            s.quit()

            return {
                "message": "Email has been sent successfully on your email address",
                "status": True
            }
        except Exception as exception:
            print(exception)
            return {
                "error": "Error while sending an email",
                "status": False
            }

    def forgot_password(self, recipient, subject,template):
        """Function for sending otp on email if user forgets password"""
        try:
            message = EmailMessage()
            message.add_alternative(Environment().from_string(template).render(
                    title='Hello World!'
                ))
            # message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            s = smtplib.SMTP('localhost')
            s.send_message(message)
            s.quit()
            # body = MIMEText(content,"html")
            return {
                "message": "OTP has been sent successfully on your email address",
                "status": True
            }
        except Exception as exception:
            print(exception)
            return {
                "message": "Error while sending an email",
                "status": False
            }


# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import logging
# import smtplib,ssl
# from jinja2 import Environment        # Jinja2 templating

# CHARSET = "UTF-8"


# port  = 25
# password = "Radixweb@13"
# smtp_server = "192.168.100.101"
# SENDER_EMAIL="anirudh.chawla@radixweb.com"

# class EmailManager:
#     server = smtplib.SMTP(smtp_server,port)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()

#     def __init__(self) -> None:
#         try:
#             self.server.login(SENDER_EMAIL,password)
#         except Exception as e:
#             logging.debug(e)
    
#     def sendEmail(self,recepient,subject,content,project_id,assignee_id):
#         TEMPLATE = '''
# <!DOCTYPE html>
# <html>
# <body>

# <h1>Verification to assign project</h1>

# <p>Click on verify button to get access of the project you have been assigned</p>


# <form action="http://127.0.0.1:8000/taskapp/index/{0}/{1}/" method="post">

#     <input type="submit" value="Verify" />
# </form>
# <p id="demo"></p>
# </body>
# </html>
# '''.format(project_id,assignee_id)
#         try:
#             body = MIMEText(
#     Environment().from_string(TEMPLATE).render(
#         title='Hello World!'
#     ), "html"
# )
#             message = MIMEMultipart("alternative")
#             message["Subject"] = subject
#             message["From"] = SENDER_EMAIL
#             message["To"] = recepient
#             # body = MIMEText(content,"html")
#             message.attach(body)
#             self.server.sendmail(SENDER_EMAIL,recepient,message.as_string())
#             return {
#                 "message":"Email has been sent successfully on your email address",
#                 "status":True
#             }
#         except Exception as e:
#             print(e)
#             return {
#                 "message":"Error while sending an email",
#                 "status":False
#             }

#     # my code
#     def forgot_password(self, recipient, subject,template):
#         """Function for sending otp on email if user forgets password"""
#         try:
#             body = MIMEText(
#                 Environment().from_string(template).render(
#                     title='Hello World!'
#                 ), "html"
#             )
#             message = MIMEMultipart("alternative")
#             message["Subject"] = subject
#             message["From"] = SENDER_EMAIL
#             message["To"] = recipient
#             # body = MIMEText(content,"html")
#             message.attach(body)
#             self.server.sendmail(SENDER_EMAIL, recipient, message.as_string())
            
#             return {
#                 "message": "OTP has been sent successfully on your email address",
#                 "status": True
#             }
#         except Exception as exception:
#             print(exception)
#             return {
#                 "message": "Error while sending an email",
#                 "status": False
#             }

    # Akash sir's code
    # def forgot_password(self, recipient, subject,template):
    #     """Function for sending otp on email if user forgets password"""
    #     try:
    #         message = EmailMessage()
    #         message.add_alternative(Environment().from_string(template).render(
    #                 title='Hello World!'
    #             ))
    #         print("scdscds")
    #         # message = MIMEMultipart("alternative")
    #         message["Subject"] = subject
    #         message["From"] = SENDER_EMAIL
    #         message["To"] = recipient
    #         s = smtplib.SMTP('localhost')
    #         s.send_message(message)
    #         s.quit()
    #         # body = MIMEText(content,"html")
    #         return Response(
    #                 ResponseData.success_without_data(
    #                     "OTP has been sent successfully on your email address"),
    #                 status=status.HTTP_200_OK,
    #             )
    #         # {
    #         #     "message": "OTP has been sent successfully on your email address",
    #         #     "status": True
    #         # }
    #     except Exception as exception:
    #         print(exception)
    #         return {
    #             "message": "Error while sending an email",
    #             "status": False
    #         }

