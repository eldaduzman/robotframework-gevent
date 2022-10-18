*** Settings ***
Documentation       A simple test with gevent library
...                 Initialize the library, creates a bundle, add keywords as coroutines and execute the coroutines.

Library             Collections
Library             String
Library             GeventLibrary
Library             SeleniumLibrary
Library             RequestsLibrary


*** Variables ***
${URL}                                      https://www.epochconverter.com/
${BROWSER}                                  Chrome
${MAIN_PAGE_PAGE_CONTAINER_LOCATOR}         id:mobilemenulink
${MAIN_PAGE_EPOCH_CLOCK_TEXTBOX_LOCATOR}    xpath://input[@id='ecinput']
${MAIN_PAGE_EPOCH_CLOCK_BUTTON_LOCATOR}     xpath://form[@id='ef']//button[@type='submit']


*** Test Cases ***
Test1
    [Documentation]    Simple test flow with gevent greenlets
    Log    Hello World
    Create Gevent Bundle    alias=alias1
    Add Coroutine    selenium test    alias=alias1
    Add Coroutine    SPT    alias=alias1
    Add Coroutine    GET    https://jsonplaceholder.typicode.com/posts/1    alias=alias1
    Add Coroutine    Sleep    time_=8s    alias=alias1
    ${values}    Run Coroutines    alias=alias1
    Log Many    @{values}
    ${jsonplaceholder_resp}    Get From List    ${values}    2
    Status Should Be    200    ${jsonplaceholder_resp}
    Should Be Equal As Strings    1    ${jsonplaceholder_resp.json()['userId']}


*** Keywords ***
SPT
    Sleep    5s

selenium test
    [Documentation]    This test opens up epoch converter UI
    ...    asserts texts

    [Teardown]    Close All Browsers
    Open Browser    ${URL}    ${BROWSER}
    Set Window Size    1000    800
    Wait Until Element Is Enabled    ${MAIN_PAGE_PAGE_CONTAINER_LOCATOR}
    Wait Until Element Is Enabled    ${MAIN_PAGE_EPOCH_CLOCK_TEXTBOX_LOCATOR}
    Wait Until Element Is Enabled    ${MAIN_PAGE_EPOCH_CLOCK_BUTTON_LOCATOR}
    ${button_content}    Get Text    ${MAIN_PAGE_EPOCH_CLOCK_BUTTON_LOCATOR}
    Should Be Equal As Strings    ${button_content}    Timestamp to Human date
