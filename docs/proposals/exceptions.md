# How do we handle exceptions?

* Status: Accepted
* Deciders: [Piotr] <!-- optional -->
* Date: 2021-11-23

## Work context

We want to be smart about how we use exceptions in the app. We want to use them as indicators that something has gone wrong or unexpected in the code. For example, if the functions registry could be loaded we want to throw and error specific to that case and handle it with an appropriate message.

## Proposal

We know that exceptions in python can be subclassed and caught accordingly to a level of ancestory.

We suggest using this pattern to throw case specific exceptions grouped in by kind and handle the most generic case in case nothing matched.

In order to make this happen and support this feature out of the box without having to remember about handling errors, we want to use a decorator that will wrap each respective command.

The decorator needs to handle each implemented error which is why creating a common base class to inherit exceptions from may save some code.

When implemented, the way for handling an unexpected behavior should be a simple as created a class that inherits from a base error class.

```python
class DocumentationQualityError(FunctionBaseError):
    code = "documentation.not_yet_the_quality"
    msg_template = 'Message to return to the user on error'
```

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus

