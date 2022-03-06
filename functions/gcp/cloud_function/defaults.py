"""Stores default classes for the Cloud Function service"""

from typing import ClassVar

from pydantic.main import BaseModel

from functions import logs
from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.constants import CloudProvider
from functions.constants import CloudServiceType
from functions.constants import RequiredFile
from functions.gcp.cloud_function.constants import Runtime
from functions.gcp.cloud_function.constants import SignatureType
from functions.gcp.cloud_function.constants import TriggerType
from functions.gcp.constants import DEFAULT_GCP_REGION
from functions.protocols import Default
from functions.system import add_file
from functions.types import PathStr


def generate_dockerfile_content(function: FunctionRecord) -> str:
    """Generates Dockerfile content for a GCP resource"""

    # TODO: To be updated when tackling generic docker runtimes
    # Consider if this is the best place to handle this and implications on other types
    # Perhaps this should be stored in the cloud function module.
    return """
# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

ARG TARGET="main"
ARG SOURCE="main.py"
ARG SIGNATURE_TYPE="event"

# Copy local code to the container image.
ENV FUNC_TARGET ${TARGET}
ENV FUNC_SOURCE ${SOURCE}
ENV FUNC_SIGNATURE_TYPE ${SIGNATURE_TYPE}
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file/59812588
ENV PYTHONUNBUFFERED TRUE

# Create the directory if it does not exist
WORKDIR "/function_home"
COPY . .

# Install production dependencies. Keeping separate for cloud functions
RUN pip install functions-framework
RUN pip install -r requirements.txt

# Add a healthcheck (Removing for the time being)
# HEALTHCHECK --interval=5m --timeout=3s \
#   CMD curl -f http://localhost/ || exit 1

# Run the web service on container startup.
CMD exec functions-framework --source=${FUNC_SOURCE}\
    --target=${FUNC_TARGET}\
    --signature-type=${FUNC_SIGNATURE_TYPE}
    """


class HTTP(Default, BaseModel):
    """Default implementation of the Cloud Function HTTP function type"""

    DEFAULT_PORT: ClassVar[int] = 8080

    @classmethod
    def config(cls, f_name: str, f_dir: PathStr) -> FunctionConfig:
        """Instantiate a default function config for the HTTP function type"""

        signature_type = SignatureType.HTTP
        config = FunctionConfig.default(
            cloud_provider=CloudProvider.GCP,
            cloud_service_type=CloudServiceType.CLOUD_FUNCTION,
            function_dir=str(f_dir),
            function_name=f_name,
            port=cls.DEFAULT_PORT,
            runtime=Runtime.PYTHON39,
            signature_type=signature_type,
            trigger=TriggerType.HTTP,
            region=DEFAULT_GCP_REGION,
        )

        config.deploy_variables.allow_unauthenticated = False

        logs.debug(f"Generated a default Pubsub config instance: {config}")
        return config

    @classmethod
    def generate_dockerfile(cls, function: FunctionRecord) -> None:
        """Generates a Dockerfile"""

        content = generate_dockerfile_content(function)
        add_file(function.config.path, RequiredFile.DOCKERFILE, content)

    @classmethod
    def generate_entry_point(cls, function: FunctionRecord) -> None:
        """Generates an entry point script with a default http example content"""

        content = """
def main(request):
    \"""HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    \"""
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)
        """
        add_file(function.config.path, RequiredFile.ENTRY_POINT, content)


class PubSub(Default, BaseModel):
    """Default implementation of the Cloud Function PubSub function type"""

    DEFAULT_PORT: ClassVar[int] = 8090

    @classmethod
    def config(cls, f_name: str, f_dir: PathStr) -> FunctionConfig:
        """Instantiate a default function config for the Pubsub function type"""

        signature_type = SignatureType.PUBSUB
        config = FunctionConfig.default(
            cloud_provider=CloudProvider.GCP,
            cloud_service_type=CloudServiceType.CLOUD_FUNCTION,
            function_dir=str(f_dir),
            function_name=f_name,
            port=cls.DEFAULT_PORT,
            runtime=Runtime.PYTHON39,
            signature_type=signature_type,
            trigger=TriggerType.PUBSUB,
            trigger_value="",
            region=DEFAULT_GCP_REGION,
        )

        logs.debug(f"Generated a default HTTP config instance: {config}")
        return config

    @classmethod
    def generate_dockerfile(cls, function: FunctionRecord) -> None:
        """Generates a Dockerfile"""

        content = generate_dockerfile_content(function)
        add_file(function.config.path, RequiredFile.DOCKERFILE, content)

    @classmethod
    def generate_entry_point(cls, function: FunctionRecord) -> None:
        """Generates an entry point script with a default pubsub example content"""

        content = """
def main(event, context):
    \"""Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    Returns:
        None. The output is written to Cloud Logging.
    \"""
    import base64

    print(\"""This Function was triggered by messageId {} published at {} to {}
    \""".format(context.event_id, context.timestamp, context.resource["name"]))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))
    return "Made it!"
        """
        add_file(function.config.path, RequiredFile.ENTRY_POINT, content)
