# Interesting way to guard your scripts from being imported by other scripts
# Not sure if an anti-pattern or not
from .gcp import app as gcp
from .new import app as new
