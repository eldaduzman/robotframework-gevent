*** Settings ***
Library         GeventLibrary    patch_thread=True
Library         SSHLibrary
Library         Collections
Library         String
Library         RequestsLibrary
Variables       ssh-vars.py


*** Test Cases ***
Gevent Test
    [Setup]    Login To VM
    Create Gevent Bundle    alias=gevent_test
    Add Coroutine    Log To Console    ASync function1    alias=gevent_test
    Add Coroutine    Log To Console    ASync function2    alias=gevent_test
    Run Coroutines    alias=gevent_test
    [Teardown]    Close Connection
    # Evaluate    from gevent import monkey;monkey.patch_thread(threading=False)


*** Keywords ***
Login To VM
    Open Connection    ${REMOTE_IP}
    Login    ${SSH_USERNAME}    ${SSH_PASSWORD}
