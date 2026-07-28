import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings


def send_email(to_email: str, subject: str, html_body: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"[email_service] Failed to send email to {to_email}: {e}")
        return False


def send_appointment_confirmation(to_email: str, patient_name: str, doctor_name: str,
                                   appointment_date: str, language: str = "en") -> bool:
    if language == "ta":
        subject = "உங்கள் மருத்துவ நேரம் உறுதி செய்யப்பட்டது"
        body = f"""
        <p>அன்பான {patient_name},</p>
        <p>உங்கள் நேரம் <b>Dr. {doctor_name}</b> உடன் <b>{appointment_date}</b> அன்று உறுதி செய்யப்பட்டுள்ளது.</p>
        <p>நன்றி,<br/>{settings.SMTP_FROM_NAME}</p>
        """
    else:
        subject = "Your Appointment is Confirmed"
        body = f"""
        <p>Dear {patient_name},</p>
        <p>Your appointment with <b>Dr. {doctor_name}</b> on <b>{appointment_date}</b> has been confirmed.</p>
        <p>Thank you,<br/>{settings.SMTP_FROM_NAME}</p>
        """
    return send_email(to_email, subject, body)


def send_appointment_cancellation(to_email: str, patient_name: str, doctor_name: str,
                                   appointment_date: str, language: str = "en") -> bool:
    if language == "ta":
        subject = "உங்கள் மருத்துவ நேரம் ரத்து செய்யப்பட்டது"
        body = f"<p>அன்பான {patient_name},</p><p>Dr. {doctor_name} உடனான {appointment_date} நேரம் ரத்து செய்யப்பட்டுள்ளது.</p>"
    else:
        subject = "Your Appointment was Cancelled"
        body = f"<p>Dear {patient_name},</p><p>Your appointment with Dr. {doctor_name} on {appointment_date} has been cancelled.</p>"
    return send_email(to_email, subject, body)
