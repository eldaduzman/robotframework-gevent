# robotframework-gevent
Run keywords asynchronously with the power of gevent

![stable](https://img.shields.io/static/v1?label=status&message=alpha&color=red)



## installation:
```
>>> pip install robotframework-gevent
```

## Usage:

```
# simple-test.robot
*** Settings ***
Documentation       A simple test with gevent library
...                 Initialize the library, create a session, add keywords as coroutines and execute the coroutines.
Library    String
Library             GeventLibrary


*** Test Cases ***
Test1
    Log    Hello World
    Create Session    alias=alias1
    Add Coroutine    Sleep Wrapper    alias=alias1
    Add Coroutine    Sleep    1s    alias=alias1
    Add Coroutine    Convert To Lower Case    UPPER
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}

*** Keywords ***
Sleep Wrapper
    Sleep    1s
```
### run command:
```
>>> robot simple-test.robot
```
## Motivation

In the modern world, software architecture is no longer the old server-client, but an event driven architecture where event happen simultaneously.
To test such a system we need the ability to run coroutines in our test scripts.

With the power of gevent, we can run several coroutines in greenlets, so integrating them into our robotframework test script will provide super powers to our testing efforts!

## File structure
```

|   LICENSE
|   .gitignore
|   .pylintrc
|   pyproject.toml
|   poetry.lock
|   README.md

|           
+---src
|   \---GeventLibrary
|       |   \---keywords
|       |       |   __init__.py
|       |       |   genvet_keywords.py
|       |   __init__.py
|       |   genvet_keywords.py
|               
+---atests
|   |   __init__.robot
|   |   simple-test.robot
|   |   
|   \---utests

```
## Code styling
### `black` used for auto-formatting code [read](https://pypi.org/project/black/),
### `pylint` used for code linting and pep8 compliance [read](https://pypi.org/project/pylint/),
### `mypy` used for type hinting [read](https://pypi.org/project/mypy/),
### `robocop` static code analyzer for robotframework [read](https://pypi.org/project/robotframework-robocop/),
### `perflint` pylint extension for performance linting [read](https://betterprogramming.pub/use-perflint-a-performance-linter-for-python-eae8e54f1e99)

## links
1. [Robotframework](https://robotframework.org/)
2. [gevent](http://www.gevent.org/)