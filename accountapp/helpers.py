from django.core.mail import send_mail
from django.conf import settings
import os
import requests
from FunctionFolder.UserConfig import *

API_KEY = "5062ce7d9da0996fc84ee29da30113c4-623424ea-bcdb87d7"
DOMAIN = "mg.lalchandomain.com"

# def send_simple_message():
def send_genflyo_mail():
    # send_mail("It works!", "This will get sent through Mailgun",
    #       "Anymail Sender <info.genflyo@gmail.com>", ["lalchanbadsa984@gmail.com"])
  	return requests.post(
  		# "https://api.mailgun.net/v3/sandboxd62d1a154de345f58e3a954ce851182c.mailgun.org/messages",
  		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
  		# auth=("api", os.getenv('API_KEY', 'API_KEY')),
  		auth=("api", API_KEY),
  		data={"from": "Lalchan Badsa <info.genflyo@gmail.com>",
			"to": "lalchanbadsa984@gmail.com",
  			"subject": "Hello mohammad pervez",
  			"text": "Congratulations mohammad pervez, you just sent an email with Mailgun! You are truly awesome!"})

# def send_genflyo_mail():
#     subject = 'You are account Activated Link'
#     message = f'Hello, I am Lalchan Badsa. Welcome my palace.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ["pervez.cto@gmail.com"]
#     send_mail(subject, message, email_from, recipient_list)
    # return True

def send_activation_mail1(email, first_name):
    subject = 'You are account Activated Link'
    message = f'Hi {first_name}, \nPlease click on the link confirm your registration and activation email:\n {main_url}/course/driver-activate-mail/{email}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_activation_mail(email, first_name, domain, uid, token):
    subject = 'You are account Activated Link'
    message = f'Hi {first_name}, \nPlease click on the link confirm your registration and activation email:\n {main_url}/account/driver-activate/{uid}/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_forget_reset_password_mail(email, token):
    subject = 'Your forget reset password link'
    message = f'Hi, click on the link to reset your password {main_url}/useraccount/seller/change_password/reset/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def reset_password_successfully_message(email):
    subject = 'Password Reset Successfully Message'
    message = f'Thank, Your Password reset successfully'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

#customer password reset start
def customer_send_forget_reset_password_mail(email, token):
    subject = 'Your forget reset password link'
    message = f'Hi, click on the link to reset your password {main_url}/reset-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def customer_reset_password_successfully_message(email):
    subject = 'Password Reset Successfully Message'
    message = f'Thank, Your Password reset successfully'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

#customer password reset end


def password_change_successfully_message(email):
    subject = 'Password Change Successfully Message'
    message = f'Thank, Your Password change successfully'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def General_Log_Message_Send(email, subject, process_name, time, error):
    subject = subject
    message = f'Process Name: {process_name}, \n Time: {time} \n Error: {error}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
