"""
Used by the packagining environment to support python package invocation - `python -m functions ...`
"""

from functions.main import app

package_name = "functions"
app(prog_name=package_name)
