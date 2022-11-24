from typing import Dict
from framework.clients.http_client import HttpClient
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from models.email import EmailRequest

logger = get_logger(__name__)


class SendInBlueClient:
    def __init__(
        self,
        configuration: Configuration
    ):
        self.__http_client = HttpClient()
        self.__api_key = configuration.send_in_blue.get(
            'api_key')
        self.__base_url = configuration.send_in_blue.get(
            'base_url')

    def __get_headers(
        self
    ):
        return {
            'Content-Type': 'application/json',
            'api-key': self.__api_key
        }

    async def send_email(
        self,
        email: EmailRequest
    ) -> Dict:
        logger.info(f'Sending email: {email.recipient}')

        response = await self.__http_client.post(
            url=f'{self.__base_url}/smtp/email',
            headers=self.__get_headers(),
            json=email.get_request())

        logger.info(f'Response: {response.status_code}')
        content = response.json()

        return {
            'response': content,
            'content': email.get_request()
        }
