# What interface should we use it interact with GCP resources?

* Status: Accepted
* Deciders: [Piotr]
* Date: 2021-11-23

## Context and Problem Statement

Since we want to enable users to be able to deploy functions to GCP, we need to have an interface that we can call within our code.

This interface needs to be capable of bridging us from a source files to a deployed and working cloud resource.

### Assumptions

The tool is not meant to be ideal, but be a working proof of concept at this point in time.

### Constraints

* Limited development capacity
* Scope of the initial release

## Decision Drivers

* Development complexity
* Short vs long term solution

## Considered Options

* `gcloud`
* `Python API`

### `gcloud`

Use the `gcloud` command line interface to move our resources from the source to cloud.

Pros:

* Good, because it is a simple solution that allows us to provide this functionality.
* Good, because it handles a lot of the complexity, like authorization, outputs, logging.

Cons:

* Bad, because it feels more like a hack than a solution.
* Bad, because it is not a long term solution.
* Bad, because it requires an external interface - `gcloud` - to handle the tasks.

**Spike**: This works relatively well, but feels like a hacky way to solve this problem.

### Python APIs

Use resource [specific](https://cloud.google.com/python/docs/reference/cloudfunctions/latest) as well as [generic](https://github.com/googleapis/google-api-python-client) python SDKs to interact with GCP resources.

Pros:

* Good, because it gives us a lot of flexibility over our implementation.
* Good, because we don't have to rely on a user having to install a tool within the environment.
* Good, because there is place for factoring out common code from different providers and exploring unification efforts more achievable.

Cons:

* Bad, because it requires a lot of additional work to write logic to handle all the resources.
* Bad, because it is much more complex to do so. There are no single call APIs for cloud functions.
* Bad, because it feels like reinventing parts of the `gcloud` tool.

**Spike**: What seems like a simple task of deploying a folder of files into a cloud function scope turns out to be more complex than that. You need to have a place to store the files, build the function and then connect all these resources. Cleaning and managing artefacts becomes our scope as well.

## Decision Outcome

Chosen option: `gcloud`, because the development effort is minimal and allows us to perform really powerful stuff. It offloads the effort onto another tool and allows us to test and move at relatively fast pace. At a cost of not being a future proof solution.

## Decision Impact

No one is impacted by this decision. Interface will stay without a change. This change does have a long term impact of being vulnerable to any `gcloud` version changes.

### How will this decision be communicated to the public

No need.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
