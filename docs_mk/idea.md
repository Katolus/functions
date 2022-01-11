In this document we discuss the purpose behind making this project and some of its criteria, expectations and scope.

## Pitch

`functions` - a command line tool that helps with managing functions as a service (FaaS) components locally and remotely.

## Background

Across the recent years and even more so in the future ones, every a developer would have worked with a serverless function. We use it to power our logic that can filtered down to a single action. Building a single point API. Building a triggered pipeline. We choose this technique for its merits in scaling and decoupling from any other part of the system. One thing goes in and something happens or is returns as a result.

It is easy to deploy a slighly tailor version of a templated function to fit your basics needs. It gets a little bit more complicated if you are facing a task that is out of ordinery. How do you keep track of your work? How do you deploy the function? How do you test it?

Not an easy task and it is not even close to being fast. Usually you need to deploy the function to see any results. Some of the providers offer helpful libraries/tools that allow you to run your serverless functions locally, but even that gets a bit complicated and requires you to spend time on learning another repository.

All this is, combined with automations you build will be highly specific to the provider you are using by which point you are locked in.

One of the things that made [HashiCorp](https://www.hashicorp.com/) products so great is that they allow for flexibility. That becoming far more important nowadays that it ever was.

In order to tackle all these pain-points and made any serverless task a much more fun experience, we propose building a software tool that takes care of all the local environment, deployment, tracking, logging and provider specific logic and gives developer a homogenus(check) CLI interface to interact with their FaaS components. It will take away the complexity and give back a modular and intuitive work tool for everyone to use.

## Progress so far

The projects started as a solo project in between job. The scope was massively undercut from the start. It is a battleground for growing developer skills and it has been treated like that, still yet to see it's first release.

## Objectives

- Fail and learn.
- Experiment and test out various ideas.
- Provide value to at least one person.
- Get people interested.

## Principle Values

- Easy to Use
- Safe
- Simple

## Timeframe

| Stage         | Summary                                                                                                      | Delivery                    |
| ------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------- |
| First Release | First release targets a somehow stable alpha version with enough functionalities to test the idea in action. | Planned for the end of 2021 |


## Engineering budget

In the first stage, the project is being developed by a single person as a side project between jobs.
Since that person has other commitments, the project has taken a lower priority, and work on it goes slower than anticipated.

So if you believe in this project, the repository is set up to support community contributions if people value it enough to contribute.

## Monitoring and Evaluation

Project is being reviewed at lest every month to reevaluate timeframes, view project interactions and adjust documentation accordingly.

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

**08/01/2021**
- Update the content to have a more holistic view.
