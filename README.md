# robotframework-gevent
Run keywords asynchronously with the power of gevent

![Coverage Status](./reports/coverage-badge.svg)


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
    [Documentation]    Simple test flow with gevent greenlets
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

## Why gevent?

Concurrency can be achieved in 3 different ways:

1.  Multiprocessing - running each task in it's own `process`.
    The cons of such an approach would be massive consumption of resources, namely CPU and memory, as this means to allocate an entire `memory heap` to each task.
    Another problem is a possible need for `Inter-Process Communication (IPC)` that might be costly.

2.  Multithreading - running each task in a `thread`.
    Unlike multiprocessing, now all tasks run on the same memory heap and separated by threads, which the CPU coordinates using `round-robin`.
    However, python's  `Global Interpreter Lock` (GIL) prevents these threads from acting concurrently, it might perform context switching when IO operation occurs but there's no control for that.


3.  Asynchronous IO - running all tasks on a single thread, while IO operations won't block the progress of the program, while code execution is committed by an   `event loop` that `selects` between attached `coroutines`.
    This is highly efficient in resources consumption when compared to multithreading and multiprocessing, but it requires some modifications to the original code.
    `Blocking` IO statements can hog the event loop and the code will not be concurrent.
    `gevent` allows programmers to write seemingly regular "blocking" python code, but it will enforce asynchronous IO compliance by `monkey patching`

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
3. [Mutation testing with cosmic-ray](https://python.plainenglish.io/python-mutation-testing-with-cosmic-ray-4b78eb9e0676)