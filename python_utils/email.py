
# coding: utf-8

# In[ ]:


import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

    SERVER = "exp-shost-01"
    FROM = from_email #'fhatt@expedia.com'
    TO = to_email_list #["fhatt@expedia.com"]  # must be a list
    SUBJECT = subject #"ALERT - SHPM LOGS "
    CONTENT = content #'hello world'
    TEXT = CONTENT.encode('utf-8')

    # Prepare actual message
    message = """    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail
    server = smtplib.SMTP(SERVER)
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


def send_html(from_email, to_email, subject, content):

    server = "exp-shost-01"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(content, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(server)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()
    
    log.debug('Email Sent')
    

