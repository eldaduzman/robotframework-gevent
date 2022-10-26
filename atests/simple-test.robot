*** Settings ***
Documentation       A simple test with gevent library
...                 Initialize the library, creates a bundle, add keywords as coroutines and execute the coroutines.

Library             Collections
Library             String
Library             GeventLibrary
Library             RequestsLibrary
Library             ./pylibs/__init__.py

Test Teardown       Clear All Bundles


*** Test Cases ***
Test1
    [Documentation]    Simple test flow with gevent greenlets
    Log    Hello World
    Create Gevent Bundle    alias=alias1
    Sleep    5s    alias=alias1    # synchronous keyword
    Add Coroutine    Sleep Wrapper    alias=alias1
    Add Coroutine    Sleep    time_=10s    alias=alias1
    Add Coroutine    Sleep    5s    alias=alias1
    Add Coroutine    GET    https://jsonplaceholder.typicode.com/posts/1    alias=alias1
    Add Coroutine    Convert To Lower Case    UPPER
    Add Coroutine    Convert To Integer    1
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}
    ${jsonplaceholder_resp}    Get From List    ${values}    3
    Status Should Be    200    ${jsonplaceholder_resp}
    Should Be Equal As Strings    1    ${jsonplaceholder_resp.json()['userId']}

Test2
    [Documentation]    Simple test flow with gevent greenlets
    Create Gevent Bundle    alias=alias2
    Add Coroutine    Wrapper1    alias=alias2
    Add Coroutine    Wrapper2    alias=alias2
    Add Coroutine    Sleep    10s    alias=alias2
    Add Coroutine    Sleep    10s    alias=alias2
    Add Coroutine    Sleep    10s    alias=alias2
    Add Coroutine    Sleep    15s    alias=alias2
    ${values}    Run Coroutines    alias=alias2    gevent_pool_size=40
    Log Many    @{values}

Test3
    [Documentation]    Testing a concurrent keyword with threads
    Create Gevent Bundle    alias=alias1
    Add Coroutine    Sleep Threading    2    7    alias=alias1
    Add Coroutine    Sleep    5s    alias=alias1
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}

Test4
    [Documentation]    Testing a concurrent keyword with processes
    Create Gevent Bundle    alias=alias1
    Add Coroutine    Sleep Processing    2    7    alias=alias1
    Add Coroutine    Sleep    5s    alias=alias1
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}

Test5
    [Documentation]    Testing a concurrent keyword with gevent
    Create Gevent Bundle    alias=alias1
    Add Coroutine    Sleep Gevent Coros    3    7    alias=alias1
    Add Coroutine    Sleep    5s    alias=alias1
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}
Test6
    [Documentation]    Testing a concurrent keyword with asyncio
    Create Gevent Bundle    alias=alias1
    Add Coroutine    Sleep Asyncio    3    7    alias=alias1
    Add Coroutine    Sleep    5s    alias=alias1
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}


*** Keywords ***
Wrapper1
    Sleep    10s
    Log    Hi
    RETURN    Some output

Wrapper2
    Sleep    10s

Sleep Wrapper
    Sleep    10s
