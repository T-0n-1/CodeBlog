*** Settings ***
Documentation        This is the test suite for the login functionality in the TalentAdore application.

Library              Browser
Resource             ../resources/common_keywords.resource
Resource             ../resources/register/register.keywords.resource

Suite Setup          New Browser        ${BROWSER}            ${HEADLESS}
Suite Teardown       Close Browser


*** Test Cases ***
Register New User
    [Documentation]    Test case for registering a new user.
    [Setup]                 Open New Tab ${URL} In Browser
    Wait For Elements State                         ${REGISTER_BUTTON}      visible
    Click                   ${REGISTER_BUTTON}
    Fill Register Form      ${USERNAME}             ${PASSWORD}
    [Teardown]              Close Context
