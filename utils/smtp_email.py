import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class SMTPEmail:
    """
    A utility class for sending emails using SMTP.

    Attributes:
        smtp_server (str): The SMTP server address.
        smtp_port (int): The port used for the SMTP server.
        username (str): The sender's email address or SMTP username.
        password (str): The sender's email password.
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        receiver_emails: list[str] | None = None,
        cc_emails: list[str] | None = None,
        bcc_emails: list[str] | None = None
    ):
        """
        Initialize the EmailSender with SMTP credentials.

        Args:
            smtp_server (str): SMTP server address.
            smtp_port (int): Port number for the SMTP server.
            username (str): Username/email used to log in to the SMTP server.
            password (str): Password for the SMTP account.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.receiver_emails = receiver_emails
        self.cc_emails = cc_emails
        self.bcc_emails = bcc_emails

    def send_email(
        self,
        subject: str,
        html_body: str,
        image_path=None,
    ):
        """
        Sends an email to recipients.

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
            msg["From"] = ", ".join(self.username)
            msg["To"] = ", ".join(self.receiver_emails)
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
                server.login(self.username, self.password)
                text = msg.as_string()
                all_recipients = (
                    self.receiver_emails
                    + (self.cc_emails if self.cc_emails else [])
                    + (self.bcc_emails if self.bcc_emails else [])
                )
                server.sendmail(self.username, all_recipients, text)
                logging.info(f"Email sent successfully to: {self.receiver_emails}")
        except Exception as send_email_exception:
            raise Exception(f"Unable to send email: {send_email_exception}.")

    def send_demo_email(self):
        """
        Sends a demo email using a predefined template.
        """
        subject = "Demo Email Subject"
        body = (
            "Hello,\n\n"
            "This is a demo email sent using the EmailSender class.\n"
            "Best regards,\n"
            "Your Friendly Bot"
        )
        self.send_email(subject=subject, html_body=body)

    def send_template_email(self):
        """
        
        """


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    smtp_host = os.getenv("SMTP_ADDRESS")
    smtp_user = os.getenv("SMTP_ACCOUNT")
    smtp_pswd = os.getenv("SMTP_PASSWORD")
    smtp_port = os.getenv("SMTP_PORT")
    email_recipient = ['sinkukumar.r@hq.grapxhsys.com']

    smtp_email = SMTPEmail(smtp_host, smtp_port, smtp_user, smtp_pswd, email_recipient)
    smtp_email.send_demo_email()
