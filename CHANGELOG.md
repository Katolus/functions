# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2022-03-03

### Added

* [Local]: Generate new template function directories for starting new functions. Two types GCP `http`/`pubsub`.
* [Local]: Add an existing **function** to the function registry to be run and deployed as functions native to the package.
* [Local]: Build pre-generated, validated and **locally** existing functions using Docker.
* [Local]: Operate (`deploy`/`remove`) Google Cloud Platform functions from a local machine.
* [Local]: Store information about the built, run and deployed functions locally for reference and configuration.
* [Local]: Print out information about functions and their statuses (Build/Deployed/Running) using the [list](**link to api document**) command.
* [Local]: Log function history using a log file stored on your local device.
* [GCP]: Deploy locally existing functions as cloud functions. Limited to two types - `http` and `pubsub`.
* [GCP]: Delete functions deployed to GCP using this package.

[Unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...HEAD
[0.0.1]: https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1
