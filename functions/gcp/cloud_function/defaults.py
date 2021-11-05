from typing import ClassVar

from pydantic.main import BaseModel

from functions.config.models import FunctionConfig
from functions.constants import CloudProvider
from functions.constants import CloudServiceType
from functions.gcp.cloud_function.constants import Runtime
from functions.gcp.cloud_function.constants import SignatureType
from functions.gcp.cloud_function.constants import Trigger
from functions.gcp.constants import DEFAULT_GCP_REGION
from functions.types import PathStr


class HTTP(BaseModel):
    DEFAULT_PORT: ClassVar[int] = 8080

    @classmethod
    def config(cls, function_name: str, function_dir: PathStr) -> FunctionConfig:
        signature_type = SignatureType.HTTP
        config = FunctionConfig.default(
            cloud_provider=CloudProvider.GCP,
            cloud_service_type=CloudServiceType.CLOUD_FUNCTION,
            function_dir=str(function_dir),
            function_name=function_name,
            port=cls.DEFAULT_PORT,
            runtime=Runtime.PYTHON39,
            signature_type=signature_type,
            trigger=Trigger.HTTP,
            region=DEFAULT_GCP_REGION,
        )

        config.deploy_variables.allow_unauthenticated = False
        return config


class PubSub(BaseModel):
    DEFAULT_PORT: ClassVar[int] = 8090

    @classmethod
    def config(cls, function_name: str, function_dir: PathStr) -> FunctionConfig:
        signature_type = SignatureType.PUBSUB
        return FunctionConfig.default(
            cloud_provider=CloudProvider.GCP,
            cloud_service_type=CloudServiceType.CLOUD_FUNCTION,
            function_dir=str(function_dir),
            function_name=function_name,
            port=cls.DEFAULT_PORT,
            runtime=Runtime.PYTHON39,
            signature_type=signature_type,
            trigger=Trigger.HTTP,
            region=DEFAULT_GCP_REGION,
        )
