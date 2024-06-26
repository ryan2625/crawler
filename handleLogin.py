from bs4 import BeautifulSoup
import requests
from creds import creds
from all_pages import arr
from urllib.parse import urlparse

'''
Author: Ryan Freas
Date: 4/27/2024
'''
loginPage = "https://www.irem.org/sso/login.aspx"

def getSession(login):
    emailPage = requests.get(login)
    parsedEmailPage = BeautifulSoup(emailPage.content, "html.parser")

    payload = setASPHiddenFields(parsedEmailPage)
    payload["email"] = creds[0]
    payload["usr_btn"] = "Next"
    with requests.Session() as sesh:
        sesh.get(login)
        postVal = sesh.post(login, data=payload)
    
    passwordPage = requests.get(postVal.url)
    parsedPasswordPage = BeautifulSoup(passwordPage.content, "html.parser")

    payloadFinal = setASPHiddenFields(parsedPasswordPage)
    payloadFinal["ctl00$main$LoginTextBox"] = creds[0]
    payloadFinal["ctl00$main$PasswordTextBox"] = creds[1]
    payloadFinal["ctl00$main$SubmitButton"] = "Login"
    
    parseUrl = urlparse(postVal.url)
    toFetch = "https://my2.irem.org/SSO/LoginTemplates/DefaultLogin.aspx?" + parseUrl[4]
    sesh.get(postVal.url)
    finalURL = sesh.post(toFetch, data=payloadFinal)
    # print(sesh.cookies)
    # print(sesh.headers)
    # If login was a complete success, expect
    # to see https://www.irem.org/home
    print(finalURL.url)
    return sesh


def setASPHiddenFields(page):
    viewState = page.find("input", {"name" : "__VIEWSTATE"})["value"]
    viewStateGen = page.find("input", {"name" : "__VIEWSTATEGENERATOR"})["value"]
    eventValid = page.find("input", {"name" : "__EVENTVALIDATION"})["value"]
    payload = {"__EVENTTARGET": "", 
            "__EVENTARGUMENT": "", 
            "__VIEWSTATE":viewState, 
            "__VIEWSTATEGENERATOR":viewStateGen, 
            "__EVENTVALIDATION": eventValid,
    }
    return payload

