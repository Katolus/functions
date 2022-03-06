from typing import Dict, Generator, Optional, Tuple

from functions.docker.enums import DockerLabel

DockerBuildAPIGenerator = Generator[Tuple[Optional[str], Optional[str]], None, None]
DockerLabelsDict = Dict[DockerLabel, str]
