from pydantic.main import BaseModel

from .cloud_function.defaults import HTTP
from .cloud_function.defaults import PubSub


class GCPFunctionConfig(BaseModel):
    HTTP = HTTP()
    PubSub = PubSub()
