# `functions`

> This package that will get you working with FaaS.

[![DeepSource](https://deepsource.io/gh/Katolus/functions.svg/?label=active+issues&show_trend=true&token=NaMzVnONrQ-lLiofAWpYLilG)](https://deepsource.io/gh/Katolus/functions/?ref=repository-badge)

|   !   | This package is not ready for `production` use. The API is unstabble as it hasn't been released in any major or minor versions of it yet and is constant development. Use it at your own risk and pleasure. <br><br> **Please read the documentation carefully so there are not surprises to state of this project.** |
| :---: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

<!-- ![Logo]() -->

**Outstanding items before the first release can be viewed under [this](https://github.com/users/Katolus/projects/1) project.**

<!-- * Documentation: <https://Katolus.github.io/functions> -->
* GitHub: <https://github.com/Katolus/functions>
* PyPI: <https://pypi.org/project/functions-cli/>
* Free software: MIT

`functions` is a utility package written in Python. It is built to help the developer run, test and deploy FaaS (Function as a Service) resources. Our goal is to combine and simplify efforts required for local and cloud development.

We are using `docker` as a primary technology to build and orchestrate the functions locally.

To deploy them to a cloud provider you need to have relevant software pre-installed.

## Features

The project is still under deep development, and there is still a lot of work to be done even to reach the base quality.
Nonetheless, we believe there is value in using it as it is if it fits your needs and requirements (Python + Linux).

Feedback, issues and request are more than welcome. See how you can [contribute](CONTRIBUTING.md).

See the road map [document](./docs/roadmap.md) to see how our vision might need your future interest.

Here is a list of functionalities that the package is capable of.

### Locally

* Generate a new template function directories for starting new functions. Two types GCP `http`/`pubsub` - [tutorial](docs/examples/new_gcp_functions.md).
* Add an existing function to the function registry to be run and deployed as functions native to the package - [tutorial](docs/examples/add_existing_function.md).
* Build pre-generated, validated and **locally** existing functions using Docker **link to api document**.
* Operate (`deploy`/`remove`) Google Cloud Platform functions from a local machine - [tutorial](docs/examples/http_function.md).
* Store information about the built, run and deployed functions locally for reference and configuration - [proposal](docs/proposals/function_registry.md).
* Print out information about functions and their statuses (Build/Deployed/Running) using the [list](**link to api document**) command.
* Log function history using a log file stored on your local device - [proposal](docs/proposals/logging.md).

### GCP

* Deploy locally existing function as cloud functions. Limited to two types - `http` and `pubsub`.
* Delete functions deployed to GCP using this package.

## Compatibility

Currently the project has been developed and tested only on a Ubuntu OS with **Python 3.9** as the deployment environment. More development is in progress.

## Requirements

The package is a utility one and it requires underlying software for specific function to be available.

Minimum:

* Python >= `3.8` - for the functioning of the package.
* `docker` - for running any of the functions locally, you will need to [install docker](https://docs.docker.com/engine/install/).

    ```bash
    sudo chmod 666 /var/run/docker.sock
    ```

* [`poetry`](https://python-poetry.org/docs/#installation) - for running the source code locally and code development you need to have this package in the scope.

For GCP:

* `gcloud` - for deploying to the GCP environment, [install gcloud](https://cloud.google.com/sdk/docs/install).

## Installation

Depending on your use case there are option on how to proceed with installing the package.
It is recommended that for regular use, you install the package from `pypi` following the `For use` section.

If you plan of developing or adjust the code or underlying structures make sure to check out the `For development` section.

### For use

Since it is a regular Python package, available in the main `pypi` repository you can start using it simply by installing the package in your Python environment by running

```bash
pip install functions-cli
```

in your terminal.

### For development

Check out the [local development document](docs/local_development.md) for instructions on how get set up.

## Usage

Regardless if you installed the package from the *pypi* repository or from source code, you should be able to invoke the `functions` tool from your command line. The tool has many different commands that should help you building your serverless functions (surprise, otherwise it would be useless...).

Here are a few core ones to get you started. For a full and a comprehensive description of the `CLI` please refer to the [cli document](docs/cli.md).

Keep in mind that the package is in development and all of its structure is a subject to change.

## Creating a new FaaS

The tool allows you to quickly generate a template of a function that you can the modify to quicken your efforts in producing code.

```bash
functions new http {name_of_the_function}
```

will generate you a new `http` like template for your FaaS function in your current directory.

## Building a function

Before you start working with a function you need make sure it is built and available as a docker image. To do so, run

```bash
functions build {name_of_the_function}
```

## Running a function locally

It is great to see what we have created before deploying it to the world. Running...

```bash
functions run {name_of_the_function}
```

will start a docker container and expose the function to your locally network on a available port.

**Note**: If you haven't run this function before, you will need to make sure you built (the `build` command) the function first before running.

Please remember that the container will run as long as you leave it for, so make sure to take it down once you have done all your testing. Running...

```bash
functions stop {name_of_the_function}
```

should do the job.

## Deployment it to the cloud

Since we build software to serve us something, we most likely want to deploy it to see it all working and get that full developer satisfaction and availability.

Depending what configuration you had set up, you will be able to deploy your projects to various platforms (extended support pending).

For example to deploy a function quickly to GCP as a cloud function you want to run...

```bash
functions gcp deploy {path_to_the_function}
```

With the correct setup and permissions this should allow you to the deploy a function to the GCP directly from the `functions` cli.

## Remove a function

This command will remove a function from the local storage, but will not remove the code from the disk.

```bash
functions remove {name_of_the_function}
```

## Installing autocompletion

Core CLI functionality is built on top of [`Typer`](https://github.com/tiangolo/typer) which means that if you want autocompletion in your scripts follow the instructions derived from there.

```bash
functions --install-completion bash
```

With respect to the version of shell you are using.

## Getting help

The tool is built on brilliant software of others. One of them being `typer`. Thanks to the work of others, you can query the CLI for any useful information by adding `--help` to any of your commands.

```bash
functions run --help
```

If you stumble in to any major issue that is not described in the documentation, send a message or create an issue. We will try to help you as soon as it is possible.

## Contributing

If you are interested in helping out check out the [contributing](./CONTRIBUTING.md) document.
