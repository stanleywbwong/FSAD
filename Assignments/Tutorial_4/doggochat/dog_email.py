# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os, random, string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import sendgrid_api_key
from database import get_dog_by_handle, reset_db_password
from werkzeug.security import generate_password_hash

def send_message(handle, subject, body):

    dog = get_dog_by_handle(handle)
    name = dog['Name']
    email = dog['Email']

    message = Mail(
        from_email='stanley.wong@yale.edu',
        to_emails=email,
        subject=subject,
        html_content=body)
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def reset_password(handle):
    new_password = get_random_string(20)
    reset_db_password(handle, generate_password_hash(new_password))
    send_message(handle, 'Dogchat password reset', 'Your new password is %s' % new_password)
