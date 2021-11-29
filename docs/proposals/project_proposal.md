## Project proposal for making `functions-cli`

In this document I discuss the purpose behind making the project and some of its criteria, expectations and scopes.

**Table of Contents**

- [Project proposal for making `functions-cli`](#project-proposal-for-making-functions-cli)
- [Title](#title)
- [Status](#status)
- [Background](#background)
- [Objectives](#objectives)
- [Values](#values)
- [Goals](#goals)
- [Timeframe](#timeframe)
- [Engineering budget](#engineering-budget)
- [Monitoring and Evaluation](#monitoring-and-evaluation)
- [Lessons learned](#lessons-learned)
- [Changelog](#changelog)

## Title

  * `functions-cli` - a command line tool that helps with functions as a service (FaaS) components.

## Status

  * Work In Progress.

## Background

In 2019/2020, I worked on a project involving deploying code with cloud functions in GCP. Testing these functions in the local environment was tricky, so I had to deploy a new version to the cloud and view status, read logs, and troubleshoot from the UI for each change I made. That took, on average, about 5 minutes and obviously, I made many changes(mistakes).

The engineering efficiency was not there.

So I had an idea. I wanted to make it as easy and intuitive as possible for a user to work with the concept of FaaS. I wanted to simplify everyone's work. Take away the complexity and bring safety.

I combined that with a goal of mine of knowing more about OpenSource and started work.

After starting, the project's scope grew massively each day. What I  initially thought to be a month of work turned out to be more and more. Adjust and learn. The scope for the first release shrank down a few times since then, and there are some critical [lessons learned](#lessons-learned) there.

For now, the project is a battlefield and a workspace that I use to test out ideas, tools, design patterns and concepts with a defined and invested concept behind it.

## Objectives

- Fail and learn.
- Experiment and test out various ideas.
- Provide value to at least one person.
- Get people interested.


## Values

- Easy to Use
- Safe
- Simple

## Goals

- [ ] Get at least one person that is not a connection to contribute to the project.
- [ ] Build a python package.
- [ ] Deploy first release to `pypi`.
- [ ] Try out Github actions.
- [ ] Learn how to setup an OpenSource project.

## Timeframe

| Stage         | Summary                                                                                                      | Delivery                    |
| ------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------- |
| First Release | First release targets a somehow stable alpha version with enough functionalities to test the idea in action. | Planned for the end of 2021 |


## Engineering budget

In the first stage, the project is being developed solely by me as a side project between jobs.
Since starting a job, the project has taken a lower priority, and I work on it when I get the time.

With that said, the repository is set up to support community contributions if people value it enough to contribute.

## Monitoring and Evaluation

I hope to come back at least every month to reevaluate timeframes to view project interactions and adjust documentation accordingly.

## Lessons learned

Beyond elemental learnings such as how to pick a suitable license or which tool to use to perform a specific task, here lay the lessons with a broader, more generic scope:

- It takes a lot of time, effort and brainpower to build a quality project.
- The scope is **always** bigger than you initially thought to be.
- It is vital to build and bring tools to the project.
- Planning out the scope and writing a comprehensive overview is reasonably the most crucial step. Otherwise, you are unsure what you are trying to do or how the project should be structured. **It is worth the effort**.
- Documentation is as important if not more important than code.


## Changelog

<br>
<!-- pagebreak -->

**30/11/2021**
- Added the project proposal document.
