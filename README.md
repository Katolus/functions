# `functions-cli` 

[![DeepSource](https://deepsource.io/gh/Katolus/functions.svg/?label=active+issues&show_trend=true&token=NaMzVnONrQ-lLiofAWpYLilG)](https://deepsource.io/gh/Katolus/functions/?ref=repository-badge)

> This package that will get you working with FaaS.

|   !   | This package is not anywhere near being ready. It hasn't been released in any major or minor versions of it yet as it is constant development. Use it at your own risk and pleasure. |
| :---: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

<!-- ![Logo]() -->

**Outstanding items before the first release**: 
- Add the ability to deploy functions in languages other than just Python.
- Ability to run the package with configuration on other OS than Linux



`functions-cli` is a utility package written in Python. It is built to help the developer code, test and deploy FaaS (Function as a Service) resources. 

It is using `docker` to build and orchestrate the functions locally. To deploy them to any of the cloud providers you need to have relevant software installed and appropriate authorization to deploy them. 

## Compatibility

- Currently the project has been developed and tested only on a Linux OS with **Python 3.9** as the deployment environment.  

## Requirement

The package is a utility one and it requires underlying software for specific function to be available. 

- Python >= 3.9 - for the functioning of the package. 
- `gcloud` - for deploying to the GCP environment.
- `docker` - for running any of the functions locally.
- `poetry` - for running the source code locally. 

## Installation

Since it is a regular Python package you can start using it simply by installing the package in your Python environment by running

```console
pip install functions-cli
```

in your console.

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

```console
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

```
functions stop {name_of_the_function}
```

should do the job.

## Deployment it to the cloud

Since we build software to serve us something, we most likely want to deploy it to see it all working and get that developer satisfaction. 

Depending whether you have a configuration set up you will be able to deploy your projects to various platforms (support pending). 

For example to deploy a function quickly to GCP as a cloud function you want to run...

```console
functions gcp deploy {path_to_the_function}
```

With the correct setup and permissions this should allow you to the deploy a function to the GCP directly from the `functions` cli.  


## Clearing out resources

### Remove a function

```
functions remove {name_of_the_function}
```



## Installing autocompletion
TBU


## Getting help

The tool is built on brilliant software of others. One of them being `typer`. This allows you to query the CLI for any useful information by adding `--help` to any of your commands (useful tip to all your future work). 

```console
functions run --help
```

If you stumble in to any major issue that is not described in the documentation, send me a message. I will try to assist when possible.