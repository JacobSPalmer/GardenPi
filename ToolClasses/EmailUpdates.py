import smtplib
import time
import ssl

email_templates = {
    'plant_watered': {
        'subject': 'GardenPi Notification: Plant Watered!',
        'message': 'GardenPi has watered your plant at '
    },
    'water_level_alert': {
        'subject': 'GardenPi Notification: Check GardenPi Reserve Levels',
        'message': 'GardenPi recommends checking your water level.'
    }
}

def send_water_email(time_watered):
    port = 465
    smtp_server = "smtp.gmail.com"
    FROM = "gardenpinotice@gmail.com"
    TO = "jacob.palmer2020@gmail.com"
    password = "c264_264"
    
    subject = email_templates['plant_watered']['subject']
    message = email_templates['plant_watered']['message']
    
    complete_message = ''
    complete_message = "Subject: {}\n\n{} {}".format(subject, message, time_watered)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(FROM, password)
        server.sendmail(FROM, TO, complete_message)
        
def send_checkwater_email():
    port = 465
    smtp_server = "smtp.gmail.com"
    FROM = "gardenpinotice@gmail.com"
    TO = "jacob.palmer2020@gmail.com"
    password = "c264_264"
    
    subject = email_templates['water_level_alert']['subject']
    message = email_templates['water_level_alert']['message']
    
    complete_message = ''
    complete_message = "Subject: {}\n\n{}".format(subject, message)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(FROM, password)
        server.sendmail(FROM, TO, complete_message)
        
    