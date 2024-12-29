# Bulk Email Sender with Personalized HTML Content - (Email Automation Script)

This Python script allows you to send personalized HTML emails in bulk, attaching files as needed. It reads recipient email addresses and company names from a file, customizes the email content for each recipient, and sends it via Gmail's SMTP server.

## Features

- Bulk email sending with customizable HTML content
- Replaceable placeholders for personalization (e.g., `[Company]`)
- Optional file attachments
- Reads recipient information from a text file

## Requirements

- Python 3.x
- An app-specific password for Gmail (required for secure login)
- Dependencies:
  - `smtplib`, `email`, `os` , no need to install already there in standard py library

## Setup

1. **Install Python**: Ensure Python 3.x is installed.
2. **App-Specific Password**: Go to [Google App Passwords](https://myaccount.google.com/apppasswords) and generate an app-specific password. Use this password in place of your regular Gmail password.
3. **HTML Content**: Convert your email content to HTML using a tool like [WordHTML](https://wordhtml.com) and save it in a file (e.g., `content.txt`).
   ### Note -
   Write a email with styling, font and all then convert it into html using [WordHTML](https://wordhtml.com) tool then add it to content text file

## Usage

1. **Clone the Repository** (or download the script):

    ```bash
    git clone https://github.com/aadarsh-nagrath/dev-scriptsX.git
    cd email-automation-script
    ```

2. **Prepare Input Files**:
   - **Email Data (`emails.txt`)**: Create a file named `emails.txt` in the format:
   
     ```
     recipient1@example.com,CompanyName1
     recipient2@example.com,CompanyName2
     ```
   - **HTML Content (`content.txt`)**: Create an HTML file containing your email message. Use `[Company]` as a placeholder for the company name, which will be replaced automatically.

3. **Configure the Script**:
   - Update the `sender_email` and `sender_password` variables in the script with your email address and app-specific password.
   - Modify `subject` and `attachment_path` variables as needed.
   - Also change the `Your Name` var in script to your name.

4. **Run the Script**:

    ```bash
    python send_email.py
    ```

5. **Monitor Output**: The script will print messages to the console indicating whether each email was successfully sent or failed.

## Code Overview

### Key Functions

- **`send_email`**: Sends an email with the specified subject, body, recipient, and optional attachment.
- **`get_email_addresses_and_companies`**: Reads email addresses and company names from `emails.txt`.
- **`read_mail_body`**: Reads the HTML content from `content.txt` and replaces `[Company]` with the actual company name.

## License

This project is licensed under the MIT License.
