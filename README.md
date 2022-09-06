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

Library    String
Library             GeventLibrary


*** Test Cases ***
Test1
    Log    Hello World
    Create Session    alias=alias1
    Add Coroutine    Sleep Wrapper    alias=alias1
    Add Coroutine    Sleep    20s    alias=alias1
    Add Coroutine    Sleep    10s    alias=alias1
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

Modern software architecture is `event driven`, with many background process.
Servers are being more pro-active instead of re-active as we see in a `client server` architecture.

In order to test such systems, we need the ability to run coroutines in our test scripts.

With the power of [gevent](http://www.gevent.org/), we can run several coroutines in greenlets, so integrating them into our robotframework test script will provide super powers to our testing efforts!

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