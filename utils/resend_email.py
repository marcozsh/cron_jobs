import resend
import os
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv('RESEND_API_KEY') or sys.exit("RESEND_API_KEY no está configurado en las variables de entorno.")
resend.api_key = API_KEY
FROM_EMAIL = os.getenv('FROM_EMAIL') or sys.exit("FROM_EMAIL no está configurado en las variables de entorno.")

def send_email(to, subject, html):
    response = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": to,
        "subject": subject,
        "html": html
    })
    return response