# Where do we store configuration files?

* Status: Proposed
* Deciders: [Piotr]
* Date: 2022-01-08

## Work context

We want the tool to have a easily persistent state in which information about managed functions can be stored to enable better management and enhanced development capabilities. In this document want to find a good solution of storing all the configuration files and future application specific files in a place where it can be access by all components that need it. A unified strategy that works well across different operating systems and specific OS distributions.

## Problem

Since we decided on use a file based system to persist information about the state of the tool, we face a problem of finding the base place to store it.

Unfortunately there is not a single pattern widely approved and implemented by developers working cross systems that instructs an application where to store the config data so that is best for the health of the files and the whole system.

For example linux application developers have a concept of a `XDG_CONFIG_HOME` environment variable that usually is empty but if missing they default such actions to the `.config` file on a user's workspace.

This however is unique to Linux and does not apply throughout other systems, hence we need to find a way of tackling the issue and enable usage of this application on Windows and macOS systems.

## Proposal

The solution is relatively naive and suggests using a condition based definition of a default system config path. Each OS type will point to a different config path.

```python
# Set system constants based on the current platform
if sys.platform.startswith("win32"):
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(os.environ["APPDATA"], "config")
elif sys.platform.startswith("linux"):
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(os.environ["HOME"], ".config")
elif sys.platform.startswith("darwin"):
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(
        os.environ["HOME"], "Library", "Application Support"
    )
else:
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(os.environ["HOME"], "config")
```

It is hard to make sure that all the operating systems are accounted for in this definition so an update might be required in the future.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
