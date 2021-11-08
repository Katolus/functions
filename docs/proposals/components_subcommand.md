# `components` subcommand


## Proposal

A suggestion to add a `component` subcommand together with a related module for interaction with installed and available components.

A function component would be accessible via

```
functions components docker
```

```
functions components gcp
```

An empty command would display a component's summary.

```
functions components docker

> `docker` dependency is installed and ready to be used.

or

> `docker` is not available, please make sure you install it by running `functions component docker --install` on your machine.
```

The **initial state** of the application would only be defined on creating the `config.toml` file for the first time and modified only through said `components` commands.

The information about the state of the components would be saved in the `config.toml` file and available to the app as a single source of truth for managing the state dependent scripts.

A way of resetting and rerunning the `components` validation would be to reset or remove the config file.

```
functions config --reset
```

This should not affect anything about the state of the registry.

## Goals

By implementing this, we are solving an issue of not knowing which components are available for usage.
