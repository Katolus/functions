# Logging in `functions`

* Status: Accepted
* Deciders: [Piotr] <!-- optional -->
* Date: 2022-02-23

## Work context

We want to make sure that we know what is happening with resources locally in case any information might need to be brought back or reviewed. In development as well as normal use.

## Proposal

We suggest creating a storing a simple file based log using that Python's standard library modules.

The files should take a lot of space and should ensure that the information is properly rotated.

The file is named - `functions.log` by default and is stored in the `config` module's directory path.

### Default level

The default level for command execution is `INFO`. It means that none of the debug statements will be visible in the a command's output.

### Format

A log format takes a form of three parts:

```console
{time} - {level} - {message}

2022-02-27 01:08:33,367 - DEBUG - Running application in info logging level.
```

### Command - logs

The file can be used by any regular means, like reading the file, output in terminal or terminal tailing.

In order to make this more straightforward, we added a `functions logs` command that would output and tail the log file so that you don't need to do anything else.

### Access

You can get access to the debug logging output on command execution by passing the `--verbose` flag as an option to the root `functions` command.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
