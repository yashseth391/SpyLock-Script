import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, sender_password, recipient_email, subject, body, image_path=None):
    try:
        # Connect to the SMTP server
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email, sender_password)

        # Create the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Attach an image to the email if provided
        if image_path:
            try:
                with open(image_path, "rb") as img_file:
                    img = MIMEBase('application', 'octet-stream')
                    img.set_payload(img_file.read())
                    encoders.encode_base64(img)
                    img.add_header('Content-Disposition', f'attachment; filename="{image_path.split("/")[-1]}"')
                    message.attach(img)
            except FileNotFoundError:
                print(f"Error: The file at {image_path} was not found.")

        # Send the email
        s.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")

        # Close the SMTP connection
        s.quit()

    except Exception as e:
        print(f"Failed to send email: {e}")


  

