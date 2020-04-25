import platform

from route_utils import *

app = Flask(__name__)


@app.route('/')
def index():
    if isCurrentUserAuthenticated():
        return homePageTemplate()
    else:
        return redirectionToLogin()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return loginPage()

    if request.method == 'POST':
        if isRequestedUserAuthenticated():
            setCurrentUserAuthenticated()
            return routingToRedirectionSource()
        else:
            return loginPageCredentialsInvalid()


@app.route('/frames', methods=['GET', 'POST'])
def frames():
    if not isCurrentUserAuthenticated():
        setRedirectionSource('frames')
        return redirectionToLogin()

    if request.method == 'GET':
        return linkTemplateDefault()

    if request.method == 'POST':
        return saveStreamFramesAndReturnLinkPage()


@app.route('/record', methods=['GET', 'POST'])
def record():
    if not isCurrentUserAuthenticated():
        setRedirectionSource('record')
        return redirectionToLogin()

    if request.method == 'GET':
        return linkTemplateDefault()

    if request.method == 'POST':
        return recordStreamFramesAndReturnLinkPage()


if __name__ == '__main__':
    createMediaFolders()

    if platform.system() == 'Linux':
        print('[ running on windows ... ] ')
        app.run(host='0.0.0.0')

    if platform.system() == 'Windows':
        print('[ running on windows ... ] ')
        app.run()
