# TODO: Add a validator that checks for correct name
def default_config(function_name: str, signature_type: str) -> dict:
    return {
        "run_variables": {
            "source": "main.py",
            "entry_point": "main",
            "signature_type": signature_type,
            "name": function_name,
            "port": 8080,
        },
        "env_variables": {},
        "deploy_variables": {
            "provider": "gcp",
            "service": "cloud_function",
            "allow_unauthenticated": False,  # Consider taking a prompt 
        },
    }


default_entry_hello_pubsub = """
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

default_entry_hello_http = """
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

default_docker_file = """

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

default_docker_ignore_file = """
# Docker specific
Dockerfile
.dockerignore

# Configuration
config.json
"""

default_requirements_file = """
"""
