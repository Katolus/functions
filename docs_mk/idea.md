Here you can find additional context on purpose behind making this project and some of its criteria, expectations and scope.

## Quick Pitch

`functions` - a command line tool that helps manage functions as a service (FaaS) components locally and remotely.

## Background

If you are a developer working with any cloud providers, the chance is, you would have heard about serverless functions. You can use them to run small, independent components that can scale on demand. Their scope is usually that of a single task. Examples include: building a single point API, building a triggered pipeline, connecting to a resource etc... It is a fantastic piece of technology that can decouple large systems and support a wide variety of cases.

Generally, it is easy to deploy a simple serverless function as a template version to fit your basic needs. It gets a little more complicated if you face a task that is out of the ordinary. Questions emerge. How do you keep track of your work? What was deployed or what was run. How do you deploy the function? How do you test it?
It is not easy to handle all that using a standard tool like the `gcloud` command-line tool, and it is not even close to being fast. Usually, you need to deploy the function to see any results. Some providers offer helpful libraries/tools that allow you to run your serverless functions locally, but even that quickly gets complicated and requires you to learn another repository and its documentation.

Even if you pass through, the automations you built will be highly specific to the provider you are using by which you are locked in.

One of the things that made [HashiCorp](https://www.hashicorp.com/) products so great is that they allow for flexibility. Flexibility and modularity are becoming far more important nowadays than it ever was.

In an attempt to tackle all these pain-points and make any serverless task a much more fun experience, we propose building a software tool that takes care of all the local environment, deployment, tracking, logging and provider-specific logic and gives a developer a homogeneous CLI interface to interact with their FaaS components. A tool that takes away the complexity and gives back an intuitive work tool for everyone to use.

## Progress so far

The project started as a solo project in between jobs. It's scope was massively undercut from the start, but with time and experience, the spectrum became something that we can track with much higher confidence. The project is a battleground for growing developer skills, and it has been treated like that, still yet to see its first release.

## Objectives

- Fail and learn.
- Experiment and test out various ideas.
- Provide value to at least one person.
- Get people interested.

## Principle Values

- Easy to Use.
- Safe.
- Simple.

## Timeframe

| Stage         | Summary                                                                                                      | Delivery                    |
| ------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------- |
| First Release | The first release targets a stable alpha version with enough functionalities to test the idea in action. | Planned for the end of 2021 |


## Engineering budget

In the first stage, the project is being developed by a single person as a side project between jobs.
Since that person has other commitments, the project has taken a lower priority, and work on it goes slower than anticipated.

So if you believe in this project, the repository is set up to support community contributions if people value it enough to contribute.

## Monitoring and Evaluation

The project is being reviewed at least every month to reevaluate timeframes, view project interactions and adjust documentation accordingly.

## Lessons learned

Beyond elemental learnings such as how to pick a suitable license or which tool to use to perform a specific task, here lay the lessons with a broader, more generic scope:

- It takes a lot of time, effort and brainpower to build a quality project.
- The scope is **always** bigger than you initially thought to be.
- It is vital to build and bring tools to the project.
- Planning out the scope and writing a comprehensive overview is reasonably the most crucial step. Otherwise, you are unsure what you are trying to do or how the project should be structured. **It is worth the effort**.
- Documentation is as important if not more important than code.
