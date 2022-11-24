from constants.features import Feature
from framework.clients.feature_client import FeatureClientAsync
from framework.rest.blueprints.meta import MetaBlueprint
from models.email import (SendDataJsonEmailRequest, SendDataTableEmailRequest,
                          SendEmailRequest)
from quart import abort, request
from services.email_service import EmailService

email_bp = MetaBlueprint('email_bp', __name__)


@email_bp.configure('/api/email/send', methods=['POST'], auth_scheme='send')
async def post_email_send(container):
    feature_client: FeatureClientAsync = container.resolve(FeatureClientAsync)
    email_service: EmailService = container.resolve(
        EmailService)

    if not await feature_client.is_enabled(Feature.EMAIL):
        return feature_client.get_disabled_feature_response(
            Feature.EMAIL)

    body = await request.get_json()
    email = SendEmailRequest(
        data=body)

    if not email.validate():
        abort(404)

    return await email_service.send_email(
        request=email)


@email_bp.configure('/api/email/datatable', methods=['POST'], auth_scheme='send')
async def post_email_datatable(container):
    feature_client: FeatureClientAsync = container.resolve(
        FeatureClientAsync)
    email_service: EmailService = container.resolve(
        EmailService)

    if not await feature_client.is_enabled(Feature.EMAIL):
        return feature_client.get_disabled_feature_response(
            Feature.EMAIL)

    body = await request.get_json()
    email = SendDataTableEmailRequest(
        data=body)

    if not email.validate():
        abort(404)

    return await email_service.send_data_table_email(
        request=email)


@email_bp.configure('/api/email/json', methods=['POST'], auth_scheme='send')
async def post_email_json(container):
    feature_client: FeatureClientAsync = container.resolve(
        FeatureClientAsync)
    email_service: EmailService = container.resolve(
        EmailService)

    if not await feature_client.is_enabled(Feature.EMAIL):
        return feature_client.get_disabled_feature_response(
            Feature.EMAIL)

    body = await request.get_json()
    email = SendDataJsonEmailRequest(
        data=body)

    if not email.validate():
        abort(404)

    return await email_service.send_json_email(
        request=email)


@email_bp.configure('/api/email/styles', methods=['GET'], auth_scheme='send')
async def get_email_styles(container):
    email_service: EmailService = container.resolve(
        EmailService)

    return email_service.get_style_options()
