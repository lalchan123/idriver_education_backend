from django.core.mail import send_mail
import requests
import datetime
import jwt
from django.conf import settings 
from FunctionFolder.UserConfig import *
from rest_framework_simplejwt.tokens import RefreshToken



def send_activation_mail1(email, first_name):
    subject = 'You are account Activated Link'
    message = f'Hi {first_name}, \nPlease click on the link confirm your registration and activation email:\n {main_url}/course/driver-activate-mail/{email}/'
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
    
def send_user_otp_mail(email, user_otp, cts):
    subject = 'Your Login OTP'
    message = f'Your OTP: {user_otp}\nCurrent TimeStand: {cts}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True   
    
def send_event_message_mail(email, name,  message, event_title, date_time, location, hosted_by):
    subject = f'{event_title}'
    message = f'Hi {name}, this is {hosted_by} and wants to invite you in my {event_title} on {date_time} on {location}, \nMessage: {message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True  
    
def send_contact_message_mail(email, name, message, event_title, date_time, location, tabledataid, hosted_by):
    subject = f'{event_title}'
    message = f'Hi {name}, this is {hosted_by} and wants to invite you in my {event_title} on {date_time} on {location},  please click below link to confirm \nhttps://gotodawat.itb-usa.a2hosted.com/reserve/{tabledataid}\nMessage: {message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True    

def send_forget_password_email(email):
    subject = 'Your forget password link from goto dawat'
    message = f'Hi, click on the link to change your password https://itb-usa.a2hosted.com/course/change_password/{email}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
    
    
def send_change_password_email(email):
    subject = 'Your change password link from idriven'
    message = f'Hi, click on the link to change your password https://itb-usa.a2hosted.com/course/change-password/{email}/'
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
    
    
def sms_send_event(number, name,  message, event_title, date_time, location, hosted_by): 
    url = "http://bulksmsbd.net/api/smsapi";
    api_key = "JDH0JtsD2cZrHRoFNmnD";
    senderid = "8809617611017";
    number = number
    message = f'Hi {name}, this is {hosted_by} and wants to invite you in my {event_title} on {date_time} on {location}, \nMessage: {message}'
 
    data = {
        "api_key" : api_key,
        "senderid" : senderid,
        "number" : number,
        "message" : message
    };
    
    response = requests.post(url = url, data = data)
    
    return response;    
    
    
def sms_send_contact(number, name, message, event_title, date_time, location, tabledataid, hosted_by): 
    url = "http://bulksmsbd.net/api/smsapi";
    api_key = "JDH0JtsD2cZrHRoFNmnD";
    senderid = "8809617611017";
    number = number
    message = f'Hi {name}, this is {hosted_by} and wants to invite you in my {event_title} on {date_time} on {location},  please click below link to confirm \nhttps://gotodawat.itb-usa.a2hosted.com/reserve/{tabledataid}\nMessage: {message}'
 
    data = {
        "api_key" : api_key,
        "senderid" : senderid,
        "number" : number,
        "message" : message
    };
    
    response = requests.post(url = url, data = data)
    
    return response;        
    
    
    
class JWTTokenGenerator:
    @staticmethod
    def generate_token(user):
        """
        Generates a JWT token for the given user.
        """
        # Define the token payload
        payload = {
            'id': user['pk'],
            'user_id': user['user_id'],
            'email': user['email'],
            'is_active': user['is_active'],
            'is_email_verified': user['is_email_verified'],
            'is_superuser': user['is_superuser'],
            'first_name': user['first_name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # Token expiration time
            'iat': datetime.datetime.utcnow(),  # Issued at time
        }

        # Create the token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # token = RefreshToken.for_user(payload)
        # return str(token.access_token)

        return token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # return {
    #     'refresh': str(refresh),
    #     'access': str(refresh.access_token),
    # }
    return str(refresh.access_token)        