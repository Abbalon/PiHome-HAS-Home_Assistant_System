from flask_mail import Message

from PiHome import mail, app


def send_email(_email, _subject, _body):
    """
        Método estandar para mandar un correo.

        Necesita:
        @param _email:  [String] #: Direcciones a las que se va a mandar el correo
        @param _subject: string #: Asunto del correo
        @param _body: obj #: Cuerpo del correo, pueden ser str, html ...
    """
    mails = [m for m in _email]

    with mail.connect() as conn:
        mensaje = Message(
            subject=_subject,
            sender=app.config['DEFAULT_MAIL_SENDER'],  # default['DEFAULT_MAIL_SENDER'], se puede omitir
            recipients=mails,
            body=_body
        )

        conn.send(mensaje)
