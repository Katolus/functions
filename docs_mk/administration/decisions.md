We strive to deliver a consistent, trusty solution for stable development. Our project is built on a structured change request system developed by the team. We impose this process to assure work is researched, reviewed, prioritized and documented with sufficient context and expectations.

## So, how do we make decisions?

We use the following process. Each of the steps assumes a positive outcome from the stage before.

1. Write a [proposal](#proposals).
2. Review the proposal.
3. Implement a prototype.
4. Evaluate changes and implications through a functional review.
5. Categorize change as a feature or architectural decision.
6. Prior to any release, move accepted proposals into respective categories of documents - `fdrs` or `adrs`.

Hopefully after this work, all the changes are discussed and the impact is flushed out.

<!-- Include a mermaid diagram when available -->

### Proposals

Documents based on the `proposals` [template](https://github.com/Katolus/functions/blob/development/docs/templates/proposals.md).

The document describes the context and a problem that a given change is to update. Proposals include at least one solution option and supplement a range of research resources.

### ADRs - Architectural decision records

> An Architectural Decision (AD) is a software design choice that addresses a functional or non-functional requirement that is architecturally significant. - [Source](https://adr.github.io/).

Documents based on the `adrs` [template](https://github.com/Katolus/functions/blob/development/docs/templates/adrs.md).

The document targets change of an architectural nature.

### FDRs - Feature decision records

Feature documents explain why features or parts of the applications not categorized as architecture were our focus. They give context on - Why? and How?
