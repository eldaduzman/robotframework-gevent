*** Settings ***
Documentation       A simple test with gevent library
...                 Initialize the library, create a session, add keywords as coroutines and execute the coroutines.

Library             String
Library             GeventLibrary
Library             RequestsLibrary


*** Test Cases ***
Test1
    [Documentation]    Simpla test flow with gevent greenlets
    Log    Hello World
    Create Gevent Bundle    alias=alias1
    Sleep    10s    alias=alias1    # synchronous keyword
    Add Coroutine    Sleep Wrapper    alias=alias1
    Add Coroutine    Sleep    20s    alias=alias1
    Add Coroutine    Sleep    10s    alias=alias1
    Add Coroutine    GET    https://jsonplaceholder.typicode.com/posts/1    alias=alias1
    Add Coroutine    Convert To Lower Case    UPPER
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}
    Should Be Equal As Strings    1    ${values[3].json()['userId']}


*** Keywords ***
Sleep Wrapper
    Sleep    1s
