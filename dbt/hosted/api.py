
import requests
import webbrowser
import threading
import os.path
import yaml

DBT_DIR = os.path.join(os.path.expanduser('~'), '.dbt/')
HOST_FILENAME = "host.yml"
DBT_HOST_FILE = os.path.join(DBT_DIR, HOST_FILENAME)

#APP_URL = 'http://hosted-dbt.appspot.com/'
APP_URL = "http://app.getdbt.com/"
API_URL = "{}api/v1".format(APP_URL)

try:
    input = raw_input
except NameError:
    pass

class DbtAPI(object):
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        if os.path.exists(DBT_HOST_FILE):
            with open(DBT_HOST_FILE, "r") as fh:
                data = yaml.safe_load(fh)
                return data.get('access_token', None)
        else:
            return None

    def ensure_token_set(self):
        key = self.get_token()

        if key:
            return key

        token = input("Set an API token: ")

        self.set_token(token)

    def set_token(self, token):
        self.token = token

        if not os.path.exists(DBT_DIR):
            os.mkdir(DBT_DIR)

        with open(DBT_HOST_FILE, "w") as fh:
            data = {"access_token": token}
            yaml.dump(data, fh)

    def headers(self):
        return {"Authorization": "Token {}".format(self.token)}

    def get_or_create_project(self, repo):
        if not self.get_token():
            print("No token found, please log in and get your API token")
            return

        data = {
            "github_repo": repo,
        }

        print('Making request to: {}/projects/'.format(API_URL))

        r = requests.post(
            '{}/projects/'.format(API_URL),
            headers=self.headers(),
            json=data)

        if r.status_code is 200:
            return r.json
        else:
            print("Encountered an error!")
            return None

    def create_or_update_active_profiles(self, project):
        if not self.get_token():
            print("No token found, please log in and get your API token")
            return

        for profile_name in project.active_profile_names:
            print("Pushing configuration for profile {}.".format(profile_name))

            profile = project.profiles[profile_name]

            targets = profile['outputs']
            for name, values in targets.iteritems():
                print("Found target {}, pushing.".format(name))

                to_send = values
                to_send['name'] = name
                to_send['password'] = to_send['pass']
                to_send['dbtype'] = to_send['type']
                del to_send['pass']
                del to_send['type']

                r = requests.post('{}/profiles/'.format(API_URL),
                                  headers=self.headers(),
                                  data=to_send)

                print(r.__dict__)
        return None

    def authenticate(self):
        if not webbrowser.open_new(APP_URL):
            raise RuntimeError("Couldn't open web browser")

        return None
