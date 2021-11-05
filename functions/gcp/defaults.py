"""Stores default classes for GCP"""

from pydantic.main import BaseModel

from .cloud_function.defaults import HTTP
from .cloud_function.defaults import PubSub


class CloudFunctionDefaults(BaseModel):
    """Links cloud function defaults together"""

    HTTP = HTTP()
    PubSub = PubSub()


class GCPDefaults(BaseModel):
    """Links GCP defaults together"""

    CloudFunction = CloudFunctionDefaults()
