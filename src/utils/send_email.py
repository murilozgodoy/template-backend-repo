from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config.settings import get_settings


def send_email(email: str, content: str, subject: str):
    """
    Envia um email usando SendGrid

    Args:
        email: Email do destinatario
        content: Conteudo HTML do email
        subject: Assunto do email
    """
    settings = get_settings()
    if settings.sendgrid_api_key is None:
        raise RuntimeError("SENDGRID_API_KEY nao configurado")

    message = Mail(
        from_email=settings.sendgrid_from_email,
        to_emails=email,
        subject=subject,
        html_content=content,
    )

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key.get_secret_value())
        response = sg.send(message)
        return {
            "status_code": response.status_code,
            "body": response.body,
            "headers": response.headers,
        }
    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        raise e
