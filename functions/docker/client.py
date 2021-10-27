"""Stores logic related to a docker client"""

import docker

docker_client: docker.client = None
if not docker_client:
    docker_client = docker.from_env()
