from pydantic.main import BaseModel

from .cloud_function.defaults import HTTP
from .cloud_function.defaults import PubSub


class CloudFunctionDefaults(BaseModel):
    HTTP = HTTP()
    PubSub = PubSub()


class GCPDefaults(BaseModel):
    CloudFunction = CloudFunctionDefaults()
