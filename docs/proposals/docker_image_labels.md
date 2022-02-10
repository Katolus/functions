# How do we define docker image labels?

* Status: Proposed
* Deciders: [Piotr] <!-- optional -->
* Date: 11-02-2022

## Context

Working with `Docker` images locally.

## Problem

We want to find a way of ensuring a future proof solution for labeling docker images, so that they are easily distinguishable, retrievable

## Criteria

* `Docker` images need to be unique
* Labels are future proof
* Don't cause any issues (no interference)
* No security issues
* [Optional] Related to labels in other resources like cloud functions (if it makes sense)

## Research

Done web research on available standards. Compared labeling strategies from some of the major projects. Looked into existing images available locally.

## Proposal

### Option 1

Use a set of generated labels defined by own standards.

Prototype iteration labels (for reference).

```text
package.functions.config
package.functions.config_path
package.functions.function_name
package.functions.function_path
package.functions.organisation
```

We propose labels having follow structure.

```text
<!-- org.{org-name}.{project-name}.image.{label} -->
```

Examples.

```text
org.ventress.functions.image.name="http-worker"
org.ventress.functions.image.config.path="/home/user/workspace/http-worker/config.json"
```

This should align with Docker's recommendations.

> Authors of third-party tools should prefix each label key with the reverse DNS notation of a domain they own, such as com.example.some-label.

### Option 2

Use a schema proposed by the community called [`label-schema`](http://label-schema.org/rc1/).

```text
org.label-schema.{label}
```

It is worth pointing out that the project is more or less unsupported and the last time was updated in `2019`.

## Decision

Based on the documentation in available on `docker.com` there is no clear indication of a standard outside of the few patterns to avoid.

Since the label schema is not something widely adapted, we will take this opportunity to experiment with `Option 1`. Use it to understand implications of defining a project owned schema and what potential influence it may have.

It should give us the best flexibility and learning spectrum without hindering potential adoptions as no future interactions are apparent at the moment.

### Predefined label list

| Label          | Description                                                      | Status            | Version |
| -------------- | ---------------------------------------------------------------- | ----------------- | ------- |
| config.content | Stringified content of a config file                             | Optional-Default  | First   |
| config.path    | Path to a config file                                            | Optional-Default  | First   |
| description    | Description of an image                                          | Optional-Default  | First   |
| mark           | Mark by which the package filters for related images - Constant  | Required-Constant | First   |
| name           | Name of a function                                               | Optional-Default  | First   |
| source         | Path to a function [Path on a System]                            | Optional-Default  | First   |
| vendor         | Constant value of the vendor managing this resource - "Ventress" | Required-Constant | First   |
| version        | Version of an image                                              | Optional-Default  | First   |

More variables in the future are to be expected.

## Resources

- http://label-schema.org/rc1/
- https://github.com/opencontainers/image-spec/blob/main/annotations.md
- https://docs.docker.com/config/labels-custom-metadata/#label-keys-and-values

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
