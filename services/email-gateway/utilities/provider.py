from clients.email_client import EmailClient
from clients.sib_client import SendInBlueClient
from framework.abstractions.abstract_request import RequestContextProvider
from framework.auth.azure import AzureAd
from framework.auth.configuration import AzureAdConfiguration
from framework.clients.feature_client import FeatureClientAsync
from framework.clients.http_client import HttpClient
from framework.configuration.configuration import Configuration
from quart import Quart, request
from services.email_service import EmailService
from framework.di.service_collection import ServiceCollection
from framework.di.static_provider import ProviderBase


class AdRole:
    SEND = 'Email.Send'


def configure_azure_ad(container):
    configuration = container.resolve(Configuration)

    # Hook the Azure AD auth config into the service
    # configuration
    ad_auth: AzureAdConfiguration = configuration.ad_auth
    azure_ad = AzureAd(
        tenant=ad_auth.tenant_id,
        audiences=ad_auth.audiences,
        issuer=ad_auth.issuer)

    azure_ad.add_authorization_policy(
        name='send',
        func=lambda t: AdRole.SEND in t.get('roles'))

    return azure_ad


class ContainerProvider(ProviderBase):

    @classmethod
    def configure_container(cls):
        container = ServiceCollection()
        container.add_singleton(Configuration)
        container.add_singleton(FeatureClientAsync)

        container.add_singleton(
            dependency_type=AzureAd,
            factory=configure_azure_ad)

        container.add_singleton(EmailClient)
        container.add_singleton(SendInBlueClient)

        container.add_transient(EmailService)

        return container
