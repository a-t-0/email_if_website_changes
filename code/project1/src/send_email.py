import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# TODO: Enable: https://myaccount.google.com/lesssecureapps


def send_email(sender_email, target_email, message, password):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)

        ## MOD
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = target_email
        msg["Subject"] = message

        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
