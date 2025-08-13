*** Settings ***
Resource    register.locators.resource


*** Keywords ***
Fill Register Form
    [Documentation]    Fills the registration form with user data.
    [Arguments]             ${username}             ${password}
    Type Text               ${REGISTER_USERNAME_FIELD}                      ${username}
    Type Text               ${REGISTER_PASSWORD_FIELD}                      ${password}
    Click                   ${REGISTER_SUBMIT_BUTTON}
