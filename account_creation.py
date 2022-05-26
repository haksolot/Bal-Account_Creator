import pyperclip
import requests
import random
import string
import time
import sys
import re
import os

SIGNUP_URL = 'https://voteicbf.pythonanywhere.com/auth/inscription'
LOGIN_URL = 'https://voteicbf.pythonanywhere.com/auth/connexion'
API = 'https://www.1secmail.com/api/v1/'
TOKEN_LINK = ""
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = random.choice(domainList)

def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]

def deleteMail():
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }


def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length != 0:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'body':
                    content = v
        linkStart = content.find('="') +2
        linkStop = content.find('">') 
        global TOKEN_LINK
        TOKEN_LINK = content[linkStart:linkStop]
        return 1
    else:
        return 0
    

####### Main code #######

while True:
    newMail = f"{API}?login={generateUserName()}&domain={domain}"
    reqMail = requests.get(newMail)
    mail = f"{extract()[0]}@{extract()[1]}"
    email = {'email' : mail}
    password = {'mdp' : 'STI2D'}
    requests.post(SIGNUP_URL, email)
    pyperclip.copy(mail)
    print(mail)
    while checkMails() == 0:
                checkMails()
    requests.post(TOKEN_LINK, password)
    print('Compte crée !')

    connexion = {'email' : mail, 'mdp' : 'STI2D'}
    resp = requests.post(LOGIN_URL, connexion)


