
import requests
import webbrowser
import threading

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

import os.path
import yaml

DBT_DIR = os.path.join(os.path.expanduser('~'), '.dbt/')
HOST_FILENAME = "host.yml"
DBT_HOST_FILE = os.path.join(DBT_DIR, HOST_FILENAME)

#APP_URL = 'http://hosted-dbt.appspot.com/'
APP_URL = "http://127.0.0.1:8000/"
API_URL = "{}api/v1".format(APP_URL)

LISTEN_PORT = 8088

response_data = {
    'handled': False
}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #import ipdb; ipdb.set_trace()
        #contents = self.rfile.read(int(self.headers['Content-Length']))
        #response_data['access_token'] = contents

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write('Hello world')

        response_data['handled'] = True

    def log_request(self, code=None, size=None):
        print('Request')

    def log_message(self, format, *args):
        print('Message')

class DbtAPI(object):
    def __init__(self):
        self.token = self.get_token()

    def headers(self):
        return {"Authorization": "Token {}".format(self.token)}

    def get_or_create_account(self, org):
        data = {
            "name": org
        }

        r = requests.post('{}/accounts/'.format(API_URL), headers=self.headers(), data=data)
        return r.json()

    def get_or_create_project(self, repo, account_id):
        pass

    def get_or_create_user_permission(self):
        pass

    def get_current_user(self):
        pass

    def get_token(self):
        if os.path.exists(DBT_HOST_FILE):
            with open(DBT_HOST_FILE, "r") as fh:
                data = yaml.safe_load(fh)
                return data.get('access_token', None)
        else:
            return None

    def set_token(self, token):
        self.token = token

        if not os.path.exists(DBT_DIR):
            os.mkdir(DBT_DIR)

        with open(DBT_HOST_FILE, "w") as fh:
            data = {"access_token": token}
            yaml.dump(data, fh)

    def authenticate(self):
        server = HTTPServer(('localhost', LISTEN_PORT), RequestHandler)

        if not webbrowser.open_new(APP_URL):
            raise RuntimeError("Couldn't open web browser")

        server.handle_request()

        if response_data.get('access_token', "") == "":
            raise RuntimeError("Bad access token: {}".format(response_data.get('access_token')))

        token = response_data['access_token']
        self.set_token(token)

        return token
