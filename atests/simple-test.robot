*** Settings ***
Documentation     Hi
Library          GeventLibrary.GeventLibrary

*** Test Cases ***
Test1
    Log    Hello World
    Sleep    1s
    Create Session
