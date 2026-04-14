import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_email(
        title: str,
        html: str,
        smtp_host: str,
        smtp_port: int,
        sender: str,
        recipients: list[str],
        username: str | None = None,
        password: str | None = None,
        use_tls: bool = True) -> bool:
    
    body = html

    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = f"[WaiwaitiPi] {title}"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            if use_tls:
                server.starttls()
            if username or password:
                server.login(username or sender, password or "")
            server.sendmail(sender, recipients, msg.as_string())
        return True
    except smtplib.SMTPException as e:
        print(f"发送失败: {e}")
        return False