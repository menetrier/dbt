import dbt.project as project

from dbt.hosted.api import DbtAPI

class HostedPushTask:
    def __init__(self, args, project):
        self.args = args
        self.project = project

    def run(self):
        api = DbtAPI()

        if not api.get_token():
            print("No token found -- please log in and get your API token.")
            return

        api.create_or_update_active_profiles(self.project)
