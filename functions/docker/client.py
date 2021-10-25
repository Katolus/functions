"""Stores logic related to a docker client"""

import docker

# TODO: Find a better way of doing this
docker_client: docker.client = None
if not docker_client:
    docker_client = docker.from_env()
