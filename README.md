# `functions-cli`

[![DeepSource](https://deepsource.io/gh/Katolus/functions.svg/?label=active+issues&show_trend=true&token=NaMzVnONrQ-lLiofAWpYLilG)](https://deepsource.io/gh/Katolus/functions/?ref=repository-badge)

> This package that will get you working with FaaS.

|   !   | This package is not anywhere near being ready. It hasn't been released in any major or minor versions of it yet as it is constant development. Use it at your own risk and pleasure. |
| :---: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

<!-- ![Logo]() -->

<!-- * Documentation: <https://Katolus.github.io/functions> -->
* GitHub: <https://github.com/Katolus/functions>
* PyPI: <https://pypi.org/project/functions-cli/>
* Free software: MIT

**Please read the documentation carefully so there are not surprises to state of this project.**

**Outstanding items before the first release**:

* Add the ability to deploy functions in languages other than just Python.
* Ability to run the package with configuration on other OS than Linux

`functions-cli` is a utility package written in Python. It is built to help the developer run, test and deploy FaaS (Function as a Service) resources. It has a gaol of combining and simplifying the effort required for local and cloud development. Its purpose is to provide a single point of entry for all FaaS related.

It is using `docker` to build and orchestrate the functions locally. To deploy them to any of the cloud providers you need to have relevant software installed and appropriate authorization to deploy them.

## Features

The project is still under deep development, and there is still a lot of work to be done even to reach the primary quality.
Nonetheless, we believe there is value in using it as it is if it fits your needs and requirements (Python + Linux).

Feedback, issues and request are more than welcome. See how you can [contribute](CONTRIBUTING.md).

See the road map document to view the vision and if it fits your interest.

Here is a list of functionalities that the package is capable of.

### Locally

* Generate a new template function directories for starting new functions. Two types GCP `http`/`pubsub`. - [tutorial](docs/examples/new_gcp_functions.md).
* Add an existing function to the function registry to be run and deployed as functions native to the package - [tutorial](docs/examples/add_existing_function.md).
* Build pre-generated, validated and **locally** existing functions using Docker **link to api document**.
* Operate (Run/Stop) GCP-Python functions on a local machine - [tutorial](docs/examples/http_function.md).
* Store the information on the built, running and deployed functions locally for reference and configuration - [proposal](docs/proposals/function_registry.md).
* Print out a [list](**link to api document**) of functions and their statuses (Build/Deployed/Running).
* Keep track of any interactions with the functions using a handy log file for storage on your local device - [proposal](docs/proposals/logging.md).

### GCP

* Deployed a locally existing function as cloud functions of two types - `http` and `pubsub`.
* Delete functions deployed to GCP using this package.

## Compatibility

* Currently the project has been developed and tested only on a Linux OS with **Python 3.9** as the deployment environment.

More testing to be done:

* MacOS
* Windows
* Different Python versions

## Requirement

The package is a utility one and it requires underlying software for specific function to be available.

* Python >= 3.9 - for the functioning of the package. Min - `3.6.2` - to enhance support of types
* `gcloud` - for deploying to the GCP environment.
* `docker` - for running any of the functions locally.
* `poetry` - for running the source code locally.

## Install

### For use

It is recommended that for regular use, you install the package from pypi.
Since it is a regular Python package, available in the main pypi repository you can start using it simply by installing the package in your Python environment by running

```bash
pip install functions-cli
```

in your terminal.

### For development

Check out the local development document for instructions on how get set up.

### Running from source code

To operate the package from the source code.

1. Download the repository.
2. Using `poetry`, install all the dependencies by running `poetry install`.
3. Run `poetry shell` to enter the scope of the package.
4. Execute or invoke the commands like you would normally, by running `functions [OPTIONS] COMMAND [ARGS] ...` in the invoked shell.

    **Additionally** you can install the package from source code by building a wheel and installing it manually in your environment's scope.

5. Run `poetry build` and you should see a `dist` folder appear in the root directory of the code (assuming you are running the command from there).
6. Install the package directly by the while specifying a path to the source - `pip install /home/{your_user}/{project_root_path}/dist/functions_cli-0.1.0a2-py3-none-any.whl`.

Handy tutorial in the scope of the `typer` package, that could help with this -> [here](https://typer.tiangolo.com/tutorial/package/).

## Usage

Regardless if you installed the package from the online repository or from the source code, you should be able to invoke the `functions` tool from your command line. The tool has many different commands that should help you building your serverless functions (surprise, otherwise it would be useless...). Here I name a few core ones, but for a full and a comprehensive description of the `CLI` please refer to the [cli document](docs/cli.md).

Keep in mind that the package is in development and all of its structure is a subject to change.

## Creating a new FaaS

The tool allows you to quickly generate a template of a function that you can the modify to quicken your efforts in producing code.

```bash
functions new http {name_of_the_function}
```

will generate you a new http like template for your FaaS function in your current directory.

## Running a function locally

A lot of us want to see and feel what we have created working first before we deploy it to the world. Running...

```console
functions run {name_of_the_function}
```

will start a docker container and expose it to your locally network on a available port.

**Note**: If you haven't run this function before it will ask you to build (the build command) the function first before running. # To be added...

Please remember that the container will run as long as you leave it for, so make sure to take it down once you have done all your testing. Running...

```bash
functions stop {name_of_the_function}
```

should do the job.

## Deployment it to the cloud

Since we build software to serve us something, we most likely want to deploy it to see it all working and get that developer satisfaction.

Depending whether you have a configuration set up you will be able to deploy your projects to various platforms (support pending).

For example to deploy a function quickly to GCP as a cloud function you want to run...

```bash
functions gcp deploy {path_to_the_function}
```

With the correct setup and permissions this should allow you to the deploy a function to the GCP directly from the `functions` cli.

## Clearing out resources

### Remove a function

```bash
functions remove {name_of_the_function}
```

## Installing autocompletion

TBU

## Getting help

The tool is built on brilliant software of others. One of them being `typer`. This allows you to query the CLI for any useful information by adding `--help` to any of your commands (useful tip to all your future work).

```bash
functions run --help
```

If you stumble in to any major issue that is not described in the documentation, send me a message. I will try to assist when possible.
