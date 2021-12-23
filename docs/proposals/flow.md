# Flow

**Status**: Work in Progress

Below describes a details flow for a user interacting with the package for the first time.

1. Installing package with `pip`.
   * Python required.
2. Running it for the first time. What is happening?
   * Since there is no `config` directory and message should be displayed warning that the `init` method needs to be run to finish setup. [To be implemented - #160, #161]
   * On running the `init` command, the config directory is created and validation on operating systems, components is run.
   * If not successful, handle any issues gracefully, disabling unavailable components and warning user about missing required components like `docker`.
   * Storing the state of the app inside the config, so that this validation is not run on every invocation of the cli.
3. Running the app next time.
   * should not go trigger previous steps (unless there is a config file missing).
   * run respective command, logging all the information
4. Config can be reset by running `functions config --reset`.
   * This would trigger a rerun of the validations required for a normal functioning of the package: `components`/...
5. In addition to a reset, components can be interacted with via the `components` subcommands.
6. Available commands will be dependant on the availability of a given components so for example `run`, `stop` will be dependent on the availability of the `docker` component.
7. Each component will have a set of rules it needs to meet in order to be considered valid (version, etc...)
