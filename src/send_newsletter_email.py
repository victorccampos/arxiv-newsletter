from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import os
from dotenv import load_dotenv
from pathlib import Path

import re


load_dotenv()

APP_PASSWORD = os.getenv("APP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

def format_html(text: str) -> str:
    """
    Remove os backticks da resposta obtida pela API do Gemini que é formatada em
    Markdown.
    """
    # Remove ```html no início e ``` no final se existirem
    padrao = r"^```(?:html)?\s*(.*?)\s*```$"
    match = re.search(padrao, text.strip(), re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    html = text.strip()
    Path("../html/newsletter_content.html").write_text(html)
        
    return html


def send_email(subject: str, html_content: str):
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    # TODO: implementar mailing list
    msg["To"] = EMAIL_TO 
    
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_FROM, APP_PASSWORD)
        smtp.send_message(msg)
