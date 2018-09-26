
# coding: utf-8

# In[ ]:


import socket
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import logging
log = logging.getLogger(__name__)
log.debug('Module loaded')


# ### Send simple email :
# Example : 
# ```
# email.send_simple(to_email_list=['jlescutmuller@expedia.com'],
#                   subject='test',
#                   content='test', 
#                   from_email='jlescutmuller@expedia.com')
# ```

# In[ ]:


def send_simple(from_email, to_email_list, subject, content):
    # If no sender is specified, please use server name (to know at least if its dev, int or prod..)
    if from_email is None or len(from_email)==0 : from_email = socket.gethostname().split('.')[0]+'@expedia.com'
    
    # Prepare actual message
    message = f"""    From: {from_email}
    To: {", ".join(to_email_list)}
    Subject: {subject}

    {content.encode('utf-8')}
    """

    # Send the mail
    server = smtplib.SMTP("exp-shost-01")
    try:
        server.sendmail(FROM, TO, message)
        server.quit()
        log.debug('Email Sent')
    except TypeError:
        log.debug('Error Sending Email')


# # Example
# to_email_list = ["fhatt@expedia.com"]
# from_email = 'fhatt@expedia.com'
# subject = 'test'
# content='hello world'
# send_email(from_email, to_email_list, subject, content)

# In[ ]:


def send_html(from_email, to_emails, subject, content, image_attachments = {}):
    # If no sender is specified, please use server name (to know at least if its dev, int or prod..)
    if from_email is None or len(from_email)==0 : from_email = socket.gethostname().split('.')[0]+'@expedia.com'
    if type(to_emails) is str : to_emails = [to_emails] # If only 1 recipient, put it in a list anyway...
    
    # Create message container - the correct MIME type is multipart/alternative.
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = from_email
    msgRoot['To'] = ", ".join(to_emails) 
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgAlternative.attach(MIMEText(content))
    msgAlternative.attach(MIMEText(content, 'html'))

    # Adding images :
    for image_name, image_path in image_attachments.items():
        fp = open(image_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', f'<{image_name}>')
        msgRoot.attach(msgImage)

    # Send the message via local SMTP server.
    s = smtplib.SMTP("exp-shost-01")
    s.sendmail(from_email, to_emails, msgRoot.as_string())
    s.quit()
    
    log.debug('Email Sent')

