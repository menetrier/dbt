import dbt.project as project
import os.path
import subprocess
import yaml
import re

from dbt.hosted.api import DbtAPI

class HostedInitializeTask:
    def __init__(self, args, project):
        self.args = args
        self.project = project

    def run(self):
        api = DbtAPI()
        org, repo = self.__get_remote()

        print(org, repo)

    def __parse(self, remote):
        name = None
        matched = re.match(r'git@github.com:(.*)\.git$', remote)
        if matched:
            name = matched.groups()[0]
        matched = re.match(r'github.com/(.*)\.git$', remote)
        if matched:
            name = matched.groups()[0]

        if name is None:
            raise RuntimeError("Invalid GitHub name? {}".format(name))

        org, repo = name.split("/", 1)
        return org, repo

    def __get_remote(self):
        # git remote get-url origin
        proc = subprocess.Popen(['git', 'remote', 'get-url', 'origin'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if len(err) > 0:
            raise RuntimeError(err.strip())

        github_url = out.strip()
        return self.__parse(github_url)
