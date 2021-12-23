# Functions architecture

In this document we try to discuss and propose the most optimal format for the application that supports described goals.

## List of components
- `FunctionRegistry`
- `Docker`
- `Cloud` (GCP, AWS, ...)

## Goals

### Hight modularity

**Problem**: We want to allow user to decide which parts of the package are required and which one's are not.

  This means that if the user only needs the local setup, then installing docker should be the only thing needs to be done and the rest of the

Some of the questions we need to answer with the solution:
- How do we figure out which components are available?
- How do we store that information?
- How do we change that state?
- Do we remove or update that information?
- Do we run any validation? If so, then when? How often?

### Components sync

**Problem**: We need to have a consistent way of knowing what is happening with various parts of the application at the lowest operational cost.

  This means we want to know which functions are currently deployed, but we don't want to run a check every time a script is run, because that is very inefficient in the CLI format.

Some of the questions we need to answer with the solution:
- How and when do we query and store the current state of the `Docker` component? Is a function running, stopped, built?


## Ideas

Here is a list of ideas in relation to described goals:
- [`components` subcommand](components_subcommand.md)


## Flow

1. A user installs the package with `pip`, nothing happens.
2. Running it for the first time:
   1. Let them know that it might take a bit more time since we are running some validations.
   2. Check for available components.
   3. Setting up a `config` directory.
   4. Storing the state of the app inside the config.
3. Running the app next time should not go throw these steps (unless there is a config file missing).
4. Config can be reset by running `functions config --reset`. (To be implemented)
5. Additional components can be interacted with via the `components` subcommands. (To be implemented)
6. Available commands will be dependant on the availability of a given components so for example `run`, `stop` will be dependent on the availability of the `docker` component.
7. Each component will have a set of rules it needs to meet in order to be considered valid (version, etc...)
