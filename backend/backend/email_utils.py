import smtplib
from email.message import EmailMessage
import os

def send_email(subject: str, body: str, to_email: str):
    """Send an email using SMTP settings from env.

    Supports local MailHog (no auth) and authenticated SMTP.
    """
    host = os.getenv('SMTP_HOST', '127.0.0.1')
    port = int(os.getenv('SMTP_PORT', os.getenv('MAIL_PORT', 1025)))
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASS')
    from_addr = os.getenv('EMAIL_FROM', 'no-reply@example.com')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_email
    msg.set_content(body)

    # Use simple SMTP; for TLS you'd need starttls and credentials
    try:
        if user and password:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.starttls()
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.send_message(msg)
    except Exception as e:
        # Bubble up so caller can log
        raise
