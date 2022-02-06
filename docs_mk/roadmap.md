To understand what this project is about, check out the idea [section](./idea.md).

Moving forward, our goal is to provide a valuable, tested, and robust tool that others can use to their benefit.

First release and core project progress can be tracked [here](https://github.com/users/Katolus/projects/1).

Once we reach the base quality, the are other project and idea that we hope to work on, given that `functions` starts providing value and receives required traction.

We plan to grow its capabilities, having some short and medium term goals in mind.

## Mission

> Make Functions as a Service (FaaS) easy to work with.

## Short-term - Current focus

### Clean up

Initial prototype bursting left chunks on inconsistent code. We want to bring cohesion and best practices to the first version of the project so that the technical debt does not creep on us in the future.

**Status**: [Planning](https://github.com/users/Katolus/projects/9/)

### AWS lambda support

We want to add support for AWS lambda functions locally and deployment.

**Status**: [Planning](https://github.com/users/Katolus/projects/5)

### Runtime support

Currently, the support for runtimes is quite limited due to the narrow scope of the initial implementation. We want to ensure anyone can use whichever runtime they want, given that it is supported.

**Status**: [Planning](https://github.com/users/Katolus/projects/3)

### Test coverage

As with any idea that made sense (will see about that) in the prototyping phase, we want to make sure that is well tested moving forward.

**Status**: [Planning](https://github.com/users/Katolus/projects/4/)

## Mid-term - What comes next

### Build-up documentation

It is a shame how much documentation is missing.

We want to make sure that there are **decision records**, **components descriptions**, **examples** and more, which users and developers can quickly reference at any time.

**Status**: Ongoing development

### Custom commands and scripts

We want to enable the user to create their enhancements to the functioning of the package by allowing the definition of custom scripts and commands.

**Status**: Idea

### GitHub source URL as a source path for a function

We want to support using a Github URL as a source for your function's source code.

**Status**: Idea

### Evaluate `Typer`

Despite the initial hype around this project, it does seem to be left out at the moment. The base package `click` seems to have much better support and extensibility.

**Status**: Idea

### Docker executable

We think that using python to execute the `functions` works well, however has it's limitations. Specifically when installing dependencies required to run deployment actions. All this can be neatly wrapped around with a Docker image, which needs to be in the scope of the package either way.

Much easier to manage system interactions contained within an image.

**Status**: Idea

## How to Get Involved

We try to organize our project goals with GitHub projects.

If there is an existing GitHub project, it is an excellent place to start aiding. If not, perhaps you can offer some expertise and lead an implementation forward.

As always, reach out if you fancy a discussion.
