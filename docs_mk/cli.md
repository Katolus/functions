All of the interactions with the tool are done via the command-line interface.

Once you install `functions`, the interface will be available to you automatically. The `functions` commands come with subcommands, so make sure you explore their purpose. If you are unsure, remember that running `functions` or `functions --help` will output practical information to your terminal.

Functions provide the ability to autocomplete commands. You can enable them by running `functions --install-completion` in the terminal.

We use automated documentation generation to surface some of the commands you mind find useful.

# `functions`

CLI tool that helps you manage your (FaaS) components.

**Usage**:

```console
$ functions [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--verbose`: Enable verbose logging  [default: False]
* `--version`: Print the version and exit
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add`: Add a function to the function registry.
* `build`: Build a function.
* `components`: Manage the components of the functions...
* `delete`: Delete a function with all its data from the...
* `gcp`: Interact with GCP functions.
* `list`: List all functions in the registry.
* `logs`: Print the logs of functions CLI.
* `new`: Create new templated functions.
* `remove`: Remove a function from the registry.
* `run`: Run a function locally using the built image.
* `stop`: Stop a function running locally.
* `sync`: Sync registry functions.

## `functions add`

Add a function to the function registry.

**Usage**:

```console
$ functions add [OPTIONS] FUNCTION_DIR
```

**Arguments**:

* `FUNCTION_DIR`: The directory of the function to add  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions build`

Build a function.

**Usage**:

```console
$ functions build [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to build  [required]

**Options**:

* `--disable-logs`: Disable build output  [default: False]
* `--help`: Show this message and exit.

## `functions components`

Manage the components of the functions package.

**Usage**:

```console
$ functions components [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `docker`: Manage the docker component.
* `gcp`: Manage the GCP component.

### `functions components docker`

Manage the docker component.

**Usage**:

```console
$ functions components docker [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `check`: Check if the docker component is available.
* `instructions`: Show instructions for the docker component.

#### `functions components docker check`

Check if the docker component is available.

**Usage**:

```console
$ functions components docker check [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `functions components docker instructions`

Show instructions for the docker component.

**Usage**:

```console
$ functions components docker instructions [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `functions components gcp`

Manage the GCP component.

**Usage**:

```console
$ functions components gcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `check`: Check if the GCP component is available.
* `instructions`: Show instructions for the GCP component.

#### `functions components gcp check`

Check if the GCP component is available.

**Usage**:

```console
$ functions components gcp check [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `functions components gcp instructions`

Show instructions for the GCP component.

**Usage**:

```console
$ functions components gcp instructions [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `functions delete`

Delete a function with all its data from the registry.

**Usage**:

```console
$ functions delete [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to delete  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions gcp`

Interact with GCP functions.

**Usage**:

```console
$ functions gcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `delete`: Deletes resources associated with a function...
* `deploy`: Deploy a function in GCP.
* `describe`: Shows information about a function deployed...
* `list`: List functions deployed to a service in GCP
* `logs`: Show logs of a function deployed to GCP.

### `functions gcp delete`

Deletes resources associated with a function in GCP.

**Usage**:

```console
$ functions gcp delete [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to delete  [required]

**Options**:

* `--help`: Show this message and exit.

### `functions gcp deploy`

Deploy a function in GCP.

**Usage**:

```console
$ functions gcp deploy [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to deploy  [required]

**Options**:

* `--help`: Show this message and exit.

### `functions gcp describe`

Shows information about a function deployed in GCP.

**Usage**:

```console
$ functions gcp describe [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of the function in registry  [required]

**Options**:

* `--help`: Show this message and exit.

### `functions gcp list`

List functions deployed to a service in GCP

**Usage**:

```console
$ functions gcp list [OPTIONS]
```

**Options**:

* `--service [cloud_function]`: Type of service to list  [default: cloud_function]
* `--help`: Show this message and exit.

### `functions gcp logs`

Show logs of a function deployed to GCP.

**Usage**:

```console
$ functions gcp logs [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: Name of the function in registry  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions list`

List all functions in the registry.

**Usage**:

```console
$ functions list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `functions logs`

Print the logs of functions CLI.

**Usage**:

```console
$ functions logs [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `functions new`

Create new templated functions.

**Usage**:

```console
$ functions new [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `http`: Create a new function that uses HTTP as a...
* `pubsub`: Create a new function that uses Google Cloud...

### `functions new http`

Create a new function that uses HTTP as a trigger.

**Usage**:

```console
$ functions new http [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to create  [required]

**Options**:

* `--dir DIRECTORY`: Path that will be used as a root path for the new function's files
* `--help`: Show this message and exit.

### `functions new pubsub`

Create a new function that uses Google Cloud Pub/Sub as a trigger.

**Usage**:

```console
$ functions new pubsub [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to create  [required]

**Options**:

* `--dir DIRECTORY`: Path that will be used as a root path for the new function's files
* `--help`: Show this message and exit.

## `functions remove`

Remove a function from the registry.

**Usage**:

```console
$ functions remove [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to remove  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions run`

Run a function locally using the built image.

**Usage**:

```console
$ functions run [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to run  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions stop`

Stop a function running locally.

**Usage**:

```console
$ functions stop [OPTIONS] FUNCTION_NAME
```

**Arguments**:

* `FUNCTION_NAME`: The name of the function to stop  [required]

**Options**:

* `--help`: Show this message and exit.

## `functions sync`

Sync registry functions.

**Usage**:

```console
$ functions sync [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `gcp`: Sync registry functions with GCP.
* `local`: Sync registry functions with Docker.

### `functions sync gcp`

Sync registry functions with GCP.

**Usage**:

```console
$ functions sync gcp [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `functions sync local`

Sync registry functions with Docker.

**Usage**:

```console
$ functions sync local [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
