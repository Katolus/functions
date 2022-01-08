# Logging in `functions`

* Status: Accepted
* Deciders: [Piotr] <!-- optional -->
* Date: 2021-11-23

## Work context

We want to make sure that we know what is happening with resources locally in case any information might need to be brought back or reviewed. In development as well as normal use.

## Proposal

We suggest creating a storing a simple file based log using that Python's standard library modules.

The files should take a lot of space and should ensure that the information is properly rotated.

The file is to be stored in the `config` module's directory path.

### Levels of logging

* Debug: Use this level for anything that happens in the program.

* Info: Use this level to record all actions that are user driven or system specific, such as regularly scheduled operations.

* Warning: Use this level to record all irregular or undesired actions.

* Error: Use this level to record any error that occurs.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
