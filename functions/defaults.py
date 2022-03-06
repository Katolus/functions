from pydantic.main import BaseModel

from functions.gcp.defaults import GCPDefaults


class Defaults(BaseModel):
    """Links to together all the default classes"""

    # Not sure if this is the best way to do this
    # but it works for now and it is convient
    GCP = GCPDefaults()


# Validate as being a good solution...
Defaults = Defaults()
