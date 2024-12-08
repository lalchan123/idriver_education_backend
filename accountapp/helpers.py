from django.core.mail import send_mail

from django.conf import settings 


def send_activation_mail1(email, first_name):
    subject = 'You are account Activated Link'
    message = f'Hi {first_name}, \nPlease click on the link confirm your registration and activation email:\n https://itb-usa.a2hosted.com/course/driver-activate-mail/{email}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_activation_mail(email, first_name, domain, uid, token):
    subject = 'You are account Activated Link'
    message = f'Hi {first_name}, \nPlease click on the link confirm your registration and activation email:\n https://itb-usa.a2hosted.com/account/driver-activate/{uid}/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_forget_reset_password_mail(email, token):
    subject = 'Your forget reset password link'
    message = f'Hi, click on the link to reset your password https://itb-usa.a2hosted.com/useraccount/seller/change_password/reset/{token}/'
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
    message = f'Hi, click on the link to reset your password http://localhost:3000/reset-password/{token}/'
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
