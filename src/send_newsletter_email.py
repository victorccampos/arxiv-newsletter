import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.message import EmailMessage # provavelmente será substituído.

from datetime import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv()

APP_PASSWORD = os.getenv("APP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

def clean_markdown_response(text: str) -> str:
    """
    Remove a formatação em Markdown da resposta obtida pela API do Gemini.
    """
    
    # Remove ```html no início e ``` no final se existirem
    padrao = r"^```(?:html)?\s*(.*?)\s*```$"
    match = re.search(padrao, text.strip(), re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()


def send_email(subject: str, html_content: str):
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    
    #msg.set_content(body)
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_FROM, APP_PASSWORD)
        smtp.send_message(msg)



if __name__ == "__main__":


    subject: str= f"My Subject"
    body: str = "Body from email"

    # send_email(subject, body)
