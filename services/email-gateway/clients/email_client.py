from email.mime.multipart import MIMEMultipart
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from deprecated import deprecated

logger = get_logger(__name__)


class EmailClient:
    def __init__(
        self,
        configuration: Configuration
    ):
        self._username = configuration.email.get('username')
        self._password = configuration.email.get('password')
        self._sender = configuration.email.get('sender')

    @deprecated
    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str
    ):

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(
            user=self._username,
            password=self._password)

        logger.info('Connected to SMTP server successfully')

        msg = MIMEMultipart()
        msg["From"] = self._sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'html'))
        logger.info('Message created')

        text = msg.as_string()

        result = server.sendmail(
            self._sender,
            recipient,
            text)

        logger.info('Mail sent successfully')
        server.quit()
        logger.info('Mail server closed')

        return result
