# `init` command

* Status: Accepted
* Deciders: [Piotr]
* Date: [2021-12-23]

## Context and Problem Statement

Many existing processes and components, like installation or `docker` require information about the initial state of the application to make sure all is run as expect. Currently there are multiple errors that come up due to missing core components when running CLI tool in a new environment.

On top of that all checks that are currently included are run on every invocation of the system, which can be avoided if we know something about the current state of the system.

We hope to create a way of initializing and storing all the required information with a single `init` command.

## Proposed Solution

We propose that the `init` would be responsible for:

* creating the `config` directory only if it the directory does not exist.
* if the directory exists it should notify the user that there already is some sort of configuration under a config path.
* create all the files like registry, config and all other required.
* store information about available components in scope.

We need to:

* add a check on script invocation that check if a config exists (efficiently) otherwise prints a message to run the init command.
* run all the necessary initialization

### Details

1. Loading file config to memory on script entry, as soon in execution as possible to avoid dependency issues (like `docker` lib initializing contact with the engine).
2. We propose creating an `init` function in the `main.py`. The function should include logic fitted to the responsibilities mentioned above.
3. Utilise existing config class and modify them to include information about different components. Dependence on `components` being available.

### Potential problems

It might be hard to require a config to be loaded prior to making any imports, but it should be one of the first things done.

## Benefits

If successfully, we should have a way of initializing and resting the state of the functions' tool.

Removing config, running `init` and syncing data (`sync` command) should gave us the power to always reset on the current state of the app.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
