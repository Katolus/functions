# `functions-cli`

Run script to executing, testing and deploying included functions.

**Usage**:

```console
$ functions-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `build`
* `gcp`: Deploy functions in GCP
* `list`: List existing functions
* `new`: Factory method for creating new functions
* `remove`
* `run`: Start a container for a given function
* `stop`

## `functions-cli build`

**Usage**:

```console
$ functions-cli build [OPTIONS] FUNCTION_PATH
```

**Arguments**:

* `FUNCTION_PATH`: Path to the functions you want to build  [required]

**Options**:

* `--force`: [default: False]
* `--help`: Show this message and exit.

## `functions-cli gcp`

Deploy functions in GCP

**Usage**:

```console
$ functions-cli gcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `delete`: Deletes a functions deployed to GCP
* `deploy`: Deploy a functions to GCP
* `describe`: Returns information about a deployed function
* `install`: Install required libraries
* `logs`: Reads log from a deployed function
* `update`: Update required libraries

### `functions-cli gcp delete`

Deletes a functions deployed to GCP

**Usage**:

```console
$ functions-cli gcp delete [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of the function you want to remove  [required]

**Options**:

* `--help`: Show this message and exit.

### `functions-cli gcp deploy`

Deploy a functions to GCP

**Usage**:

```console
$ functions-cli gcp deploy [OPTIONS] FUNCTION_DIR
```

**Arguments**:

* `FUNCTION_DIR`: Path to the functions you want to deploy  [required]

**Options**:

* `--service [cloud_function]`: Type of service you want this resource to be deploy to
* `--help`: Show this message and exit.

### `functions-cli gcp describe`

Returns information about a deployed function

**Usage**:

```console
$ functions-cli gcp describe [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `functions-cli gcp install`

Install required libraries

**Usage**:

```console
$ functions-cli gcp install [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `functions-cli gcp logs`

Reads log from a deployed function

**Usage**:

```console
$ functions-cli gcp logs [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `functions-cli gcp update`

Update required libraries

**Usage**:

```console
$ functions-cli gcp update [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `functions-cli list`

List existing functions

**Usage**:

```console
$ functions-cli list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `functions-cli new`

Factory method for creating new functions

**Usage**:

```console
$ functions-cli new [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `http`: Creates a new http directory
* `pubsub`: Creates a new pubsub directory

### `functions-cli new http`

Creates a new http directory

**Usage**:

```console
$ functions-cli new http [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of a function in alphabetic constrain [i.e new-function]  [required]

**Options**:

* `--dir PATH`: Directory that will be used as a root of the new function
* `--help`: Show this message and exit.

### `functions-cli new pubsub`

Creates a new pubsub directory

**Usage**:

```console
$ functions-cli new pubsub [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of a function in alphabetic constrain [i.e new-function]  [required]

**Options**:

* `--dir TEXT`: Directory that will be used as a root of the new function
* `--help`: Show this message and exit.

## `functions-cli remove`

**Usage**:

```console
$ functions-cli remove [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of the function you want to remove  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions-cli run`

Start a container for a given function

**Usage**:

```console
$ functions-cli run [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of the function you want to run  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions-cli stop`

**Usage**:

```console
$ functions-cli stop [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of the function you want to stop  [required]

**Options**:

* `--help`: Show this message and exit.
