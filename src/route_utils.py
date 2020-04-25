from flask import Flask, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
import os

from streaming import LiveStream

users = {
    "admin": generate_password_hash("root")
}

currentUserAuthenticated = False
redirectionSource = None

# move to config.ini
jpegFolderPath = '../media/jpeg'
videoFolderPath = '../media/video'

infoInvalidLink = 'Error: Invalid Link. Please check it and try again.'
infoSuccessfulStreamWriting = 'Success: end of streaming !!!'


def saveStreamFramesAndReturnLinkPage():
    try:
        saveStreamFramesToFolder(jpegFolderPath)
        return linkTemplateSuccess()
    except Exception as e:
        return linkTemplateInvalid()


def recordStreamFramesAndReturnLinkPage():
    try:
        recordVideoStreamToFolder(videoFolderPath)
        return linkTemplateSuccess()
    except Exception as e:
        return linkTemplateInvalid()


def saveStreamFramesToFolder(folderPath):
    print('[ saving jpeg ...] link: {}'.format(request.form['link']))

    with LiveStream(request.form['link']) as liveStream:
        liveStream.toJpeg(folderPath)

    print('[ end of saving jpeg ...] link: {}'.format(request.form['link']))


def recordVideoStreamToFolder(folderPath):
    print('[ saving video ...] link: {}'.format(request.form['link']))

    with LiveStream(request.form['link']) as liveStream:
        liveStream.toMp4(folderPath)

    print('[ end of saving video ...] link: {}'.format(request.form['link']))


def homePageTemplate():
    return "User authenticated. define routing path in URL address field /frames or /record"


def loginPage():
    return render_template('./login.html', error=None)


def loginPageCredentialsInvalid():
    error = 'Invalid Credentials. Please try again.'
    return render_template('./login.html', error=error)


def linkTemplateInvalid():
    return render_template('./streamLink.html', info=infoInvalidLink)


def linkTemplateSuccess():
    return render_template('./streamLink.html', info=infoSuccessfulStreamWriting)


def linkTemplateDefault():
    return render_template('./streamLink.html', info='')


def isCurrentUserAuthenticated():
    return currentUserAuthenticated


def setCurrentUserAuthenticated():
    global currentUserAuthenticated
    currentUserAuthenticated = True


def setRedirectionSource(routSrc):
    global redirectionSource
    redirectionSource = routSrc


def redirectionToLogin():
    return redirect(url_for('login'))


def isRequestedUserAuthenticated():
    return check_password_hash(users.get(request.form['username']), request.form['password'])


def routingToRedirectionSource():
    if redirectionSource:
        return redirect(url_for(redirectionSource))
    else:
        return "User authenticated. define routing path in URL address field /frames or /record"


def createMediaFolders():
    try:
        os.makedirs(jpegFolderPath)
        print('[ folder created ...] {} '.format(jpegFolderPath))

        os.makedirs(videoFolderPath)
        print('[ folder created ...] {} '.format(videoFolderPath))

    except Exception as e:
        print("[ mkdir failed ... ]", e.args)

