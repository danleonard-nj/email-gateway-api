from domain.email import EmailRequest, SendEmailResponse
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from httpx import AsyncClient

logger = get_logger(__name__)


class SendInBlueClient:
    def __init__(
        self,
        configuration: Configuration,
        http_client: AsyncClient
    ):
        self._http_client = http_client
        self._api_key = configuration.send_in_blue.get(
            'api_key')
        self._base_url = configuration.send_in_blue.get(
            'base_url')

    def _get_headers(
        self
    ):
        return {
            'Content-Type': 'application/json',
            'api-key': self._api_key
        }

    async def send_email(
        self,
        email: EmailRequest
    ) -> dict:
        logger.info(f'Sending email: {email.recipient}')

        response = await self._http_client.post(
            url=f'{self._base_url}/smtp/email',
            headers=self._get_headers(),
            json=email.get_request())

        logger.info(f'Response: {response.status_code}')
        content = response.json()

        return SendEmailResponse(
            response=content,
            content=email.get_request())
