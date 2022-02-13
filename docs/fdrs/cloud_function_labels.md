# How do we define cloud function labels?

* Status: Accepted
* Deciders: [Piotr] <!-- optional -->
* Date: 13-02-2022

## Context

Labeling cloud function resources in GCP so that they can be identified by our queries.

## Problem

We want to find a good way to unify labelling of resources in BQ for cloud functions (and potentially other resources as well) so that we can retrieve the information about functions created by the package and not others.

## Criteria

* We don't want to duplicates if that will be a problem in overwriting functions
* We don't want to enforce any labels that might collide with labels required by people using the tool
* We want to limit amount of labels to minimize unforeseen impacts.
* We don't want to expose any vulnerable information.
* We don't want to duplicate any information that might be retrievable from the background structures (like information characteristic to a cloud function in GCP - version/create date/etc..).
* If possible we want to create a system that can be employed on different resources, be it `cloud run` or different `provider` completely.

## Research

### Should we be using `tags` or `labels`?

> Labels can be used as queryable annotations for resources, but can't be used to set conditions on policies. Tags provide a way to conditionally allow or deny policies based on whether a resource has a specific tag. For more information, see the Tags overview.

Use `labels` over (`>`) `tags`.

### Are there any limitations to labels?

**Yes** and the requirements for labeling in GCP can be found [here](https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements).

* Each resource can have multiple labels, up to a maximum of 64.
* Each label must be a key-value pair.
* Keys have a minimum length of 1 character and a maximum length of 63 characters, and cannot be empty. Values can be empty, and have a maximum length of 63 characters.
* Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. All characters must use UTF-8 encoding, and international characters are allowed.
* The key portion of a label must be unique. However, you can use the same key with multiple resources.
* Keys must start with a lowercase letter or international character.

### Are there specific permissions needed for adding labels on resources?

A user may need to have to have a specific set of resources to able to perform this operation - [source](https://cloud.google.com/resource-manager/docs/creating-managing-labels#permissions).

Permissions needed:

* `resourcemanager.projects.update`
* `resourcemanager.projects.get`

## Proposal

Prototype iteration labels (for reference).

```text
functions-cli_function-mark="ventress"
functions-cli_function-name="http-label"
functions-cli_function-version="1"
```

For consistency reasons we propose following label structure.

```text
org-{org-name}-{project-name}-{label}
```

where `{org-name}` and `{project-name}` are constant to `ventress` and `functions` respectively.

We need to be able to filter out resources based on its origin in characteristic way.
For that purpose we will use a two labels.

* `mark` - label for having a consistent way of filtering resources. Takes on a constant value - `ventress`.
* `name` - function name used for identifying a specific function resource.
* `version` - version of the function deployed (if we had a version stored locally).

In testing scope consideration for now.

* `id` - indefinable string in case a name of a function was not enough or duplicated.

`Key=Value` examples.

```text
org-ventress-functions-name="http-label"
org-ventress-functions-mark="ventress"
org-ventress-functions-version="http-label-1"
```

## Resources

* https://cloud.google.com/resource-manager/docs/creating-managing-labels
* https://www.doit-intl.com/google-cloud-platform-resource-labeling-best-practices/
* https://cloud.google.com/resource-manager/docs/creating-managing-labels
* https://cloud.google.com/blog/products/gcp/labelling-and-grouping-your-google-cloud-platform-resources


<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
