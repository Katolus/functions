# `functions` - architecture overview

* Status: Accepted
* Deciders: [Piotr]
* Date: 2022-02-23

## Context and Problem Statement

This document describes all the architectural components used in the tool's layout.

It describes the flow of the app using defined user stories. It presents an overview of how different components fall into a complete composition.

The project's architecture has been developed in an iterative process of improvement to the base concept ([ADR-0001]), and this document will formalise the decisions and provide shape and form context.

## Users

We are taking into the account following user stories:

* user has never worked with function as a service
* user has existing functions and wants to use the tool for unification and ease of use
  * locally on the machine of work
  * remotely in the form of a repository
* machine use, as an example, being part of a CI/CD

## Goals

Goals are defined with the best effort of building towards our principle values of `simple`, `safe` and `easy to use`.

### Seamless installation

**Problem**: We want our users to have a single line, minimal-complexity installation journey.

**Driver**: Simple.

The installation should be a quick and easy process in the driver of *simplicity*. This should include all the ways of managing functions.

### Hight modularity

**Problem**: We want the user to decide which parts of the package are required and which are not.

**Driver**: Safe.

If the user only needs the local setup, installing `docker` should be the only thing required to run local commands.

Some of the questions we need to answer with the solution:

* How do we figure out which components are available?
* How do we store that information?
* How do we change that state?
* Do we remove or update that information?
* Do we run any validation? If so, then when? How often?

### All in sync

**Problem**: We need to have a consistent way of knowing what is happening with various parts of the application at the lowest operational cost.

**Driver**: Easy to use.

We want to know which functions are currently deployed. With that said, we want to avoid a scenario that runs a check every time a script is executed. It would be an inefficient process and would significantly slow down command execution.

Some of the questions we need to answer with the solution:

* How and when do we query and store the current state of the `Docker` component? Is a function running, stopped, built?

### Assumptions

Our users are technically skilled individuals or organisations with the necessary skills to operate a CLI tool.

### Constraints

No constraints at the moment.

## Decision Drivers

* Implementation complexity
* Simplicity of use
* Configurability

## Design decision

The architecture is built in an iterative process with improving the current design.

In the following sections, we describe components, their purpose and how they may interact with other parts of the design.

## Overview

`functions` is a command-line interface built on the base of the `typer` package.

It is built using Python. We use `docker` and `gcloud` to provide our core functionalities.

The tool uses an underlying file system to store and persist information about the state of the `functions`.

And that is about it. Very simple and handy.

## App Diagram

Checkout this diagram for an overview over the components building `functions`.

![Functions app diagram](../assets/diagrams/functional_layout.png)

## Flow

So how does `functions` move from a command execution to an executed state?

Here is an example interaction for basic case of CLI command.

1. User types a `functions` command in the terminal.
2. `functions` will evaluate available components and store this information in the config file. Command will raise exceptions if required components like `docker` are not present.
3. Next, it will evaluate the registry if information about this function is available and if said registry needs to be updated.
4. Depending on the command type, `docker` will be used to run or serve a targeted function.
5. If a command deploys resources to a cloud provider, we will use the correct provider to manipulate resources. Subject to authorization and sub-tool (like `gcloud`) availability.

There might be a few more steps involved depending on a specific command. Details are implementation specific and are not a part of the architecture decision.

## All the bits and pieces

In this section, we will name all of the components made into the first release to focus on their purpose.

We will flag interactions where it is fit.

For more details on each of these sections, please see the `fdrs` documentation. Documents included there will give more context than is available here.

### Python core

`functions` are a CLI tool built with Python and is essentially a long running script with lots of conditional outcomes, fancy triggers, cheeky logic and some fun comments along the way.

It runs, saves the side effects of commands in the config module, and finishes. No long-lasting processes or threads.

### Typer-based

It is a tool built using the [typer] library. `functions` wrap existing API and provide additional features and a "function" context.

### Config

We store some additional files on disk in the `config` module for configuration purposes. See related [fdr](../fdrs/config.md).

### Internal state

Withing the config module, we store:

* configuration for the current use of `functions`.
* [function registry](../fdrs/function_registry.md) data.
* log files.

### Function configuration

Each function can and should be configured via the required `config.json` file. That file is local to the tool and will not be a part of your cloud build.

This configuration is stored within a folder that holds "function" executables or is built into a function.

On running a function, the configuration is read by order of:

1. File inside the source repository.
2. Config loaded onto a built function image.

In other words, if the user has a configuration file within their directory, it will be read first. If they don't, then the image will read defaults from the image.

A source directory for a function is stored in an image built, so if the files are moved, the function (to another folder) may encounter some issues.

### Component management

As a modularity attempt, we introduced a concept of [components](../fdrs/components_subcommands.md).

There are 2 main components for now

* Docker
* gcloud

Both of them can be accessed via the available `components` command.

### Logging

`functions` produce simple logs for you to view if needed. More info in a related [fdr](../fdrs/logging.md) document.

### Exceptions

We created a custom error pattern to manage critical execution cases and handle them unified and funnelled. More info in the exceptions [fdr](../fdrs/exceptions.md).

### Docker items

For all our local system execution, we use docker images and containers as a medium to run all of the "functions".

To make sure we pick the right images and don't delete anything that we should not, we tag all our docker images with labels in a unified system. More info on the labelling [here](../fdrs/docker_image_labels.md).

### GCP resources

Similarly to `Docker` resources, all `GCP` resources are tagged with `functions` labels.

This should avoid issues listing or manipulating resources that users should not be touching. This, of course, has the downside of not being able to manage any existing resources. A user needs to deploy them with `functions` to see them within the tool's scope.

More info on cloud function labels [here](../fdrs/cloud_function_labels.md).

### Creating new resources

Say a user wants to have a go at creating a new function of their own.

We added a few helpful commands to generate a template directory that they can then use as a base for their function.

A template directory will include all the necessary files to run and deploy a function.

### Adding an existing function

Sometimes, a user might be experienced enough to have dealt with a FaaS concept before. For which we also offer a way.

Simply use the `add` command to add a function's directory into the scope of the tool, give it a name and of you go. This is the way.

There might be a few default files generated for the user in a given directory, so it is a good idea to make sure we didn't mess anything up by defaults.

### Command validation and autocomplete

Because we are a bit lazy sometimes and make mistakes more times, we added command validation and autocomplete built into a command execution.

We suggest that if a user encounters an error - simply cringe at the output and abandon the tool.

We support autocompletion of resources for all the cool users, so they can double tab it.

### Flows and Actions

In the spirit of avoiding repetition and context focus, we added the concepts of [flows and actions](../fdrs/flows_and_actions.md). A pattern for grouping user interactions and unique flows into separate scripts, so other parts of the code use it more easily.

This should enhance uniformity and provide a stable interaction experience to a user.

### Disclaimer

All these sections describe the idea of components and patterns. These are the best ideas that we came up with to handle code scalability and `functions` functionality while maintaining an experimental mindset. What is real and present in the code often escapes that.

## Decision Impact

| Interested Parties/Groups | Informed |
| ------------------------- | -------- |
| All Users                 | N/A      |

### How will this decision be communicated to the public

There is no need to communicate it to any channels as documentation is written before any releases. It is bound to the first release.


<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
[ADR-0001]: 0001_initial_setup.md
[typer]: https://typer.tiangolo.com/
