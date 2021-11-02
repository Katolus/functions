from enum import Enum


class Runtime(str, Enum):
    """
    Runtime constants for Cloud Functions.
    """
    PYTHON37 = 'python37'
    NODEJS10 = 'nodejs10'
    NODEJS12 = 'nodejs12'
    NODEJS14 = 'nodejs14'
    NODEJS8 = 'nodejs8'
    JAVA8 = 'java8'
    GO111 = 'go111'
    GO = 'go'
    PHP56 = 'php56'
    PHP70 = 'php70'
    PHP71 = 'php71'
    PYTHON35 = 'python35'
    PYTHON36 = 'python36'
    PYTHON38 = 'python38'
    CLOUD_FUNCTION = 'cloud_function'

# nodejs10: Node.js 10
# nodejs12: Node.js 12
# nodejs14: Node.js 14
# nodejs16: Node.js 16 (preview)
# php74: PHP 7.4
# python37: Python 3.7
# python38: Python 3.8
# python39: Python 3.9
# go111: Go 1.11
# go113: Go 1.13
# go116: Go 1.16 (preview)
# java11: Java 11
# dotnet3: .NET Framework 3
# ruby26: Ruby 2.6
# ruby27: Ruby 2.7
# nodejs6: Node.js 6 (deprecated)
# nodejs8: Node.js 8 (deprecated)
