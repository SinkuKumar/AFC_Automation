"""
SMTP Email
----------

This module contains classes to send emails using SMTP server. It also contains email templates for sending emails.

:module: smtp_email.py
:platform: Unix, Windows
:synopsis: Send emails using SMTP server and email templates.

:date: March 3, 2025
:author: Sinku Kumar `sinkukumar.r@hq.graphxsys.com <mailto:sinkukumar.r@hq.graphxsys.com>`
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class EmailSender:
    def __init__(
        self,
        smtp_server,
        smtp_port,
        sender_email,
        sender_password,
        cc_emails=None,
        bcc_emails=None,
    ):
        """
        Initializes the SMTP server.

        :param smtp_server: SMTP address
        :type smtp_server: str

        :param smtp_port: the SMTP port
        :type smtp_port: str

        :param sender_email: sender email
        :type sender_email: str

        :param sender_password: sender email password
        :type sender_password: str

        :param cc_emails: list of recipients
        :type cc_emails: list[str]

        :param bcc_emails: list of recipients
        :type bcc_emails: list[str]
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.cc_emails = cc_emails
        self.bcc_emails = bcc_emails

    def send_email(
        self,
        receiver_emails: list[str],
        subject: str,
        html_body: str,
        image_path=None,
    ):
        """
        Sends an email to recipients.

        :param received_emails: list of recipients
        :type received_emails: list[str]

        :param subject: subject of the email
        :type subject: str

        :param html_body: body of the email
        :type html_body: str

        :param image_path: path to the attachment
        :type image_path: str
        """
        try:
            # Create message container
            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(receiver_emails)
            msg["Subject"] = subject

            # Add CC and BCC if provided
            if self.cc_emails:
                msg["Cc"] = ", ".join(self.cc_emails)
            if self.bcc_emails:
                msg["Bcc"] = ", ".join(self.bcc_emails)

            # Attach HTML body
            msg.attach(MIMEText(html_body, "html"))

            # Attach image if provided
            if image_path:
                with open(image_path, "rb") as img_file:
                    img = MIMEImage(img_file.read())
                    img.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=os.path.basename(image_path),
                    )
                    msg.attach(img)

            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                text = msg.as_string()
                all_recipients = (
                    receiver_emails
                    + (self.cc_emails if self.cc_emails else [])
                    + (self.bcc_emails if self.bcc_emails else [])
                )
                server.sendmail(self.sender_email, all_recipients, text)
                logging.info(f"Email sent successfully to: {receiver_emails}")
        except Exception as send_email_exception:
            raise Exception(f"Unable to send email: {send_email_exception}.")


class EmailTemplate:
    # TODO: Implement templates for your email notifications here
    def demo_email_template(self, html_table, img_url=None):
        """
        HTML template for SMS email

        :param html_table: table defined with HTML tags
        :type html_table: str

        :param image_url: URL of the image
        :type image_url: str
        """
        return (
            f'Test Email – From Python Script',
            f"""
                <!DOCTYPE html>
                <html lang="en">

                <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Test Email</title>
                  <!-- CSS styles for formatting a table (dataframe) -->
                  <style>
                    table {{ width: 100%%; border-collapse: collapse; }}
                    th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                  </style>
                </head>

                <body>
                    <h1>Test Email</h1>
                    <p>This is a test email from Python script.</p>
                    <p>Below is the table:</p>
                    {html_table}

                    <p> Below is the image using url:</p>
                    
                    <img src="{img_url}" alt="Image" style="width: 100%; height: auto;">
                    
                    <p><b>NOTE:</b> This is an automated email. Please do not reply to this email.</p>
                    <p><b>Regards,</b></p>
                    <p>Python Script</p
                </body>

                </html>
        """,
        )


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    
    print(os.getcwd())
    
    smtp_server = os.getenv("SMTP_ADDRESS")
    smtp_port = os.getenv("SMTP_PORT")
    sender_email = os.getenv("SMTP_ACCOUNT")
    sender_password = os.getenv("SMTP_PASSWORD")

    receiver_email = ["sinkukumar.r@hq.graphxsys.com"]

    # Generate a dummy table
    html_table = """
        <table>
            <tr>
                <th>Column 1</th>
                <th>Column 2</th>
            </tr>
            <tr>
                <td>Value 1</td>
                <td>Value 2</td>
            </tr>
        </table>
    """

    image_url = "https://upload.wikimedia.org/wikipedia/commons/e/ed/Evolution_36_mail.png"

    email_template = EmailTemplate()
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    subject, html_body = email_template.demo_email_template(html_table=html_table, img_url=image_url)
    email_sender.send_email(receiver_email, subject, html_body)
    logging.info("Sent SMS email.")