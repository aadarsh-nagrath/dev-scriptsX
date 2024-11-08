# Note use https://wordhtml.com to convert the word data to html5

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import email.utils as email_utils

def send_email(subject, body, recipient, attachment_path, sender_email, sender_password):

    msg = MIMEMultipart()
    msg['From'] = email_utils.formataddr(("Your Name", sender_email)) # Replace "your Name" here
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # Attach the file if attachment_path is provided and the file exists
    if attachment_path and os.path.exists(attachment_path):
        attachment_name = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {attachment_name}')
            msg.attach(part)

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  
        server.starttls() 
        server.login(sender_email, sender_password)  

        # Send the email
        server.sendmail(sender_email, recipient, msg.as_string())
        print(f'Email sent to {recipient}')

    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
    finally:
        server.quit()

# Load email addresses and company names from a file
def get_email_addresses_and_companies(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    email_data = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 2: 
            email_data.append((parts[0], parts[1]))
    return email_data

# Read HTML mail content from content.txt file and replace [Company] placeholder
def read_mail_body(content_file, company_name):
    with open(content_file, 'r') as file:
        body = file.read()  # Read entire file content
    
    # Replace [Company] placeholder with actual company name
    body = body.replace("[Company]", company_name)
    
    return body

# Main execution
if __name__ == "__main__":
    print("Starting the script")
    email_file = "emails.txt"  # Path to the text file with email addresses
    content_file = "content.txt"  # Path to the email content text file

    # Sender's email and password
    sender_email = "mail@gmail.com"  # Replace with your email
    sender_password = "xxxx xxxx xxxx xxxx"  # Use an app-specific password , Go to Google app password generate one and replace here

    email_data = get_email_addresses_and_companies(email_file)

    # Loop through all email addresses and send emails
    for email, company in email_data:
        body = read_mail_body(content_file, company)
        subject = "Add your mail subject here"  # Add your subject mail here
        attachment_path = ""  # If want to attach a file with mail then add the file path here
        send_email(subject, body, email, attachment_path, sender_email, sender_password)