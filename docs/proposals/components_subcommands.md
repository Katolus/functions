# `components` subcommands

A suggestion to add a `component` subcommand together with a related module for interaction with installed and available components.

## Proposal

To enable better modular control we suggest adding a `components` root command that would be nested with commands relevant to specific components, like `docker` or `gcp` or any other future components. With this idea we hope to tackle problems with installation, troubleshooting and removal of these components.

A function component would be accessible via

```bash
functions components docker
```

```bash
functions components gcp
```

An empty command would display a component's summary.

```bash
functions components docker

> `docker` dependency is installed and ready to be used.

or

> `docker` is not available, please make sure you install it by running `functions component docker --install` on your machine.
```

## Optional arguments or nested commands

Debate if the command part for a specific command should be an argument or a nested command?

### Argument

Everything is stored inside the component method `def docker...` which makes it easier to implement if the component is small, but gets hard to maintain if for complex ones.

### Nested command

Requires more files and these files need to be placed and grouped accordingly, but the code should be more readable and extensible.

**Result**: Nested commands are preferred over argument commands in this case.

## Initial state

It is important for component status validation to know what is a state of a given component without running additional validation each time a script is run. Alternative is not run validation for component availability on every script run or not run any validation at all and throw errors if not available. To use enabling and disabling functionalities on component availability (medium priority) we can store the information about that availability in the config file and leave the user to update that if necessary.

The **initial state** of the application would only be defined on creating the `config.toml` file for the first time and modified only through said `components` commands.

The information about the state of the components would be saved in the `config.toml` file and available to the app as a single source of truth for managing the state dependent scripts.

A way of resetting and rerunning the `components` validation would be to reset or remove the config file.

```bash
functions config --reset
```

This should not affect anything about the state of the registry.

## List of components

* `docker`
* `gcp`

Maybe:

* `registry`


## Common functions

The common denominator of the component category allows us to factor out some of the common functionalities into shared commands.

* `instruction`
* `check`
* ...

## Flow

1. Installing package with `pip`.
   * Python required.
   * If it is possible would should create a configuration directory on installation. [Investigation]().
   * Maybe add a new command like `init` to prepare all the required variables.
2. Running it for the first time. What is happening?
   * If not created, we need to create a `.config` directory specific to an operating system and handle any issues gracefully.
   * Check for available components like `gcloud` to know which commands can be enabled. Throw errors if required components like `docker` are missing.
   * Storing the state of the app inside the config, so that this validation is not run on every invocation of the cli.
3. Running the app next time.
   * should not go trigger previous steps (unless there is a config file missing).
4. Config can be reset by running `functions config --reset`.
   * This would trigger a rerun of the validations required for a normal functioning of the package: `components`/...
5. In addition to a reset, components can be interacted with via the `components` subcommands.
6.
7. Available commands will be dependant on the availability of a given components so for example `run`, `stop` will be dependent on the availability of the `docker` component.
8. Each component will have a set of rules it needs to meet in order to be considered valid (version, etc...)

## Benefits

By implementing this, we are:

* solving an issue of not knowing which components are available for usage on script run
* adding an ability to the user for troubleshooting each component
* adding handy installation instructions
