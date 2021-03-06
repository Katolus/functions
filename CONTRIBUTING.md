# Contributing to `functions`

Since this is young and heavily self-developed repository, all contributors need to account for that.
Expect changes to be made quickly. Don't get used to a code structure until a first stable release.

If **anyone** wants to contribute regardless of that, please feel free to pickup/create an issue, drop a discussion post.

Share your ideas and let us make something out of nothing.

## Development and Branches

For development, please fork the repository. Next create a branch that follows the pattern of

```console
{number_of_an_issue}-{dash_separated_description}
```

where

- `number_of_an_issue` - is the issue number which was created in the main `functions` repository (issue you create in your forks are totally your call).
- `dash_separated_description` - is a short and sweet description of the topics being developed.

Example - `159-gracefully-handle-not-implemented-errors`

## Commits

We are trailing the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#specification), so please adhear to these rules so we can automated our release and changelog processes.

Summary of the rules:

- fix: A bug fix. Correlates with PATCH in SemVer
- feat: A new feature. Correlates with MINOR in SemVer
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing or correcting existing tests
- build: Changes that affect the build system or external dependencies (example - scopes: pip, docker, npm)
- ci: Changes to our CI configuration files and scripts (example scopes: GitLabCI)

## Main branch

Please keep track that we use `development` as our main branch and therefore all contribution should be done towards that branch.

## Pull Request Process

Once you are ready to contribute your changes to the main stream, follow GitHub's [instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) and created a pull request.

Please fill PR's description and make sure you include:

- A summary of changes.
- Assumptions or prerequisites if apply.
- Testing instructions.

Note: The more information you include in your PR and issue the easier it will for someone to review your work and merge it into the core.

When a PR is created, the tooling that we use (and constantly adjust) will run automated checks. After that is finished you may need to address issues reported by said tools. If everything goes green or you feel like the changes are not necessary, mark it as ready for review.

The feedback will communicated or PR gets merged in.

## Coding conventions

We use `flake8` for linting.

We use `black`, `isort` for formatting.

We use `mypy` for type validation.

Please follow these rules.

## Uncertainty

If you ever get stuck, not knowing how to do things, don't worry. All the people working in this project are wonderful and always happy to help and answer your questions.

We are here to learn, have fun and hopefully create something valuable.
