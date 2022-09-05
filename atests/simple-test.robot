*** Settings ***
Documentation       Hi
Library    String
Library             GeventLibrary.GeventLibrary


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