import dbt.project as project
from dbt.hosted.api import DbtAPI

class HostedAuthTask:
    def __init__(self, args, project):
        self.args = args
        self.project = project

    def run(self):
        api = DbtAPI()
        if api.token is not None:
            print "Already authenticatd!"
        else:
            api.authenticate()
            if api.token is not None:
                print "Authenticated successfully!"
            else:
                print "An error occurred while authenticating with GitHub"
