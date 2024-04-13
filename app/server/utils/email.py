from datetime import datetime
import smtplib
import requests
import os
import dns.resolver
from dotenv import load_dotenv
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("APP_PASSWORD")


def is_valid_email(email):
    try:
        # split email address to get domain name
        domain = email.split('@')[1]

        # get the MX record for the domain
        mx_records = []
        for mx in dns.resolver.query(domain, 'MX'):
            mx_records.append(mx.to_text().split()[1])

        # connect to the SMTP server of the domain and verify the email address
        smtp = smtplib.SMTP()
        smtp.connect(mx_records[0])
        smtp.verify(email)
        smtp.quit()

        return True
    except BaseException:
        return False
# to receive email in mail as well


def email_sending(receiver_email, otp):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        data = str(otp)
        # message sent to receiver
        response = server.sendmail(sender_email, receiver_email, data)
        print(response)
        server.quit()
        if not response:
            return {'status': 200, 'message': 'Email sent successfully'}
        else:
            return {
                'status': 500,
                'message': f'Failed to send email to {response}'}
    except smtplib.SMTPAuthenticationError:
        return {
            'status': 500,
            'message': 'Authentication Error: Invalid email or password'}
    except smtplib.SMTPException as e:
        return {'status': 500, 'message': f'Error sending email: {str(e)}'}
    except Exception as e:
        return {'status': 500, 'message': str(e)}
