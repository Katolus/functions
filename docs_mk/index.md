---
title: functions
---

Welcome to the `functions` project, an open source, curiosity-driven tool for optimizing the administration of function as a service (FaaS) technologies. Our purpose is to make it easier to build, maintain and deploy serverless functions.

## Resources

* GitHub: <https://github.com/Katolus/functions>
* PyPI: <https://pypi.org/project/functions-cli/>
* License: [MIT](https://github.com/Katolus/functions/blob/development/LICENSE)

## Features

The project is still under deep development, and there is still much work to be done even to reach the base quality. Nonetheless, we believe there is value in using it as it is if it fits your needs and requirements (Python + Linux).

Feedback, issues and request are more than welcome.

See the [road map](roadmap.md) to see how our vision might need your future interest.

In the following sections, we list a summary of the functionalities that the tool can perform.

### Locally

* Generate new template function directories for starting new functions. Two types GCP `http`/`pubsub`.
* Add an existing **function** to the function registry to be run and deployed as functions native to the package.
* Build pre-generated, validated and **locally** existing functions using Docker.
* Operate (`deploy`/`remove`) Google Cloud Platform functions from a local machine.
* Store information about the built, run and deployed functions locally for reference and configuration.
* Print out information about functions and their statuses (Build/Deployed/Running) using the [list](**link to api document**) command.
* Log function history using a log file stored on your local device.

### GCP

* Deploy locally existing functions as cloud functions. Limited to two types - `http` and `pubsub`.
* Delete functions deployed to GCP using this package.

## Additional Context

Anyone interested in additional details is invited to view the extended source of documentation directly in Github. Proposals, ADRs for people seriously inquisitive about how we built this project.
