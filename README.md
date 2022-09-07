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

Library             Collections
Library             String
Library             GeventLibrary
Library             RequestsLibrary


*** Test Cases ***
Test1
    [Documentation]    Simpla test flow with gevent greenlets
    Log    Hello World
    Create Gevent Bundle    alias=alias1 # Create a bundle of coroutines
    Sleep    10s    alias=alias1    # run your synchronous keyword
    # register all your keywords as coroutines to the gevent bundle
    Add Coroutine    Sleep Wrapper    alias=alias1
    Add Coroutine    Sleep    20s    alias=alias1
    Add Coroutine    Sleep    10s    alias=alias1
    Add Coroutine    GET    https://jsonplaceholder.typicode.com/posts/1    alias=alias1
    Add Coroutine    Convert To Lower Case    UPPER

    # Run your coroutines and get the values by order
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}

    # The 3rd coroutine was a request, take it's value
    ${jsonplaceholder_resp}    Get From List    ${values}    3

    # assert the returned response code to be 200
    Status Should Be    200    ${jsonplaceholder_resp}
    # assert that the returned `userId` field equals to 1
    Should Be Equal As Strings    1    ${jsonplaceholder_resp.json()['userId']}


*** Keywords ***
Sleep Wrapper
    Sleep    1s

```
### run test:
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
|       |   \---exceptions
|       |       |   __init__.py
|       |   \---keywords
|       |       |   __init__.py
|       |       |   gevent_keywords.py
|       |   __init__.py
|       |   gevent_library.py
|               
+---atests
|   |   __init__.robot
|   |   simple-test.robot
|   |   
|   \---utests
|       |   __init__.py
|       |   test_bundle_creation.py

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