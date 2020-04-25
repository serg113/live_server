from flask import Flask, render_template, redirect, url_for, request

from werkzeug.security import generate_password_hash, check_password_hash

from streaming import LiveStream

import os

app = Flask(__name__)

users = {
    "admin": generate_password_hash("root")
}

userAuthenticated = False

# move to config.ini
jpegFolderPath = '../media/jpeg'
videoFolderPath = '../media/video'

routPathBeforeRedirection = None

@app.route('/')
def index():
    if not userAuthenticated:
        return redirect(url_for('login'))
    else:
        return "User authenticated. define routing path in address"


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userAuthenticated
    error = None
    if request.method == 'POST':
        if not check_password_hash(users.get(request.form['username']), request.form['password']):
            error = 'Invalid Credentials. Please try again.'
        else:
            userAuthenticated = True
            if routPathBeforeRedirection:
                return redirect(url_for(routPathBeforeRedirection))
            return "User authenticated. define routing path in address"

    return render_template('./login.html', error=error)


@app.route('/frames', methods=['GET', 'POST'])
def frames():
    info = ''

    if not userAuthenticated:
        return redirectToLogin('frames')

    if request.method == 'POST':
        try:
            saveStreamFrames()
            info = 'Success: end of streaming !!!'
        except Exception as e:
            info = 'Error: Invalid Link. Please check it and try again.'

    return render_template('./streamLink.html', info=info)


@app.route('/record', methods=['GET', 'POST'])
def record():
    info = ''

    if not userAuthenticated:
        return redirectToLogin('record')

    if request.method == 'POST':
        try:
            recordStream()
            info = 'Success: end of streaming !!!'
        except Exception as e:
            info = 'Error: Invalid Link. Please check it and try again.'

    return render_template('./streamLink.html', info=info)


def redirectToLogin(routSrc):
    global routPathBeforeRedirection
    routPathBeforeRedirection =routSrc
    return redirect(url_for('login'))


def saveStreamFrames():
    with LiveStream(request.form['link']) as liveStream:
        liveStream.toJpeg(jpegFolderPath)


def recordStream():
    with LiveStream(request.form['link']) as liveStream:
        liveStream.toMp4(videoFolderPath)


if __name__ == '__main__':
    try:
        os.makedirs(jpegFolderPath)
        os.makedirs(videoFolderPath)
    except Exception as e:
        print("cannot create directory: ", e.args)
		
    app.run(host= '0.0.0.0')
	
	