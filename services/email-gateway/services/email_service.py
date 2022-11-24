from typing import Dict

import pandas as pd
from clients.sib_client import SendInBlueClient
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from models.email import (EmailRecipient, EmailRequest,
                          SendDataJsonEmailRequest, SendDataTableEmailRequest,
                          SendEmailRequest)
from pygments.styles import get_all_styles
from utilities.formatter import Formatter

logger = get_logger(__name__)


class EmailService:
    def __init__(
        self,
        client: SendInBlueClient
    ):
        self.__client = client
        self.__formatter = Formatter()

    def __get_client_request(
        self,
        request: SendEmailRequest,
        content
    ):
        return EmailRequest(
            recipient=EmailRecipient(
                name='KubeTools',
                email=request.recipient),
            subject=request.subject,
            content=content)

    async def send_email(
        self,
        request: SendEmailRequest
    ) -> Dict:
        logger.info(f'Sending email: {serialize(request.to_dict())}')

        html = self.__formatter.format_email(
            email_content=request.body,
            title=request.title)

        result = await self.__client.send_email(
            email=self.__get_client_request(
                request=request,
                content=html))

        return {
            'result': result
        }

    async def send_data_table_email(
        self,
        request: SendDataTableEmailRequest
    ) -> Dict:
        logger.info(
            f'Sending data table email: {request.recipient}')

        table = self.__formatter.format_table(
            df=pd.DataFrame(request.table),
            style=request.style)

        return await self.__client.send_email(
            email=self.__get_client_request(
                request=request,
                content=table))

    async def send_json_email(
        self,
        request: SendDataJsonEmailRequest
    ) -> Dict:
        logger.info(
            f'Sending JSON email: {request.recipient}')

        content = self.__formatter.format_json(
            data=request.json,
            style=request.style)

        return await self.__client.send_email(
            email=self.__get_client_request(
                request=request,
                content=content))

    def get_style_options(
        self
    ) -> Dict:
        return {
            'table_styles': self.__formatter.valid_styles,
            'json_styles': list(get_all_styles())
        }
