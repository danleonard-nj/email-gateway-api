from framework.abstractions.abstract_request import RequestContextProvider
from framework.di.static_provider import InternalProvider
from framework.logger.providers import get_logger
from framework.serialization.serializer import configure_serializer
from quart import Quart

from routes.email import email_bp
from routes.health import health_bp
from utilities.provider import ContainerProvider

logger = get_logger(__name__)
app = Quart(__name__)

configure_serializer(app)

app.register_blueprint(health_bp)
app.register_blueprint(email_bp)

ContainerProvider.initialize_provider()
InternalProvider.bind(ContainerProvider.get_service_provider())


@app.before_serving
async def startup():
    RequestContextProvider.initialize_provider(
        app=app)

if __name__ == '__main__':
    app.run(debug=True, port='5091')
