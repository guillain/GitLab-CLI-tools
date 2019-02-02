import os
import json
import requests
import git
from classes.filing import Filing


class Gitlab(object):
    def __init__(self, token, url="gitlab.com", version="4", user=""):
        self.token = token
        self.url = url
        self.version = version
        self.user = user

        self.api_url = 'https://{}/api/v{}'.format(self.url, self.version)
        self.params = {
            "private_token": self.token,
            "per_page": 100
        }
        self.headers = {
            "Content-Type": "application/json"
        }

    # Standard API methods
    def get(self, path, payload={}):
        return  self.request("GET", path, payload)

    def put(self, path, payload={}):
        return  self.request("PUT", path, payload)

    def post(self, path, payload={}):
        return  self.request("POST", path, payload)

    def delete(self, path, payload={}):
        return  self.request("DELETE", path, payload)

    # Generic requestor
    def request(self, method, path, payload={}):
        response = requests.request(
            method,
            '{}/{}'.format(self.api_url, path),
            data=json.dumps(payload),
            headers=self.headers,
            params=self.params
        )
        if response.text:
            return json.loads(response.text)
        return response

    # Specific requests
    def build_url(self, group_name, project_name):
        return 'https://{}:{}@{}/{}/{}.git'.format(self.user, self.token, self.url, group_name, project_name)

    def get_group(self, group_name):
        for group in self.get("groups"):
            if group_name == group['name']:
                return group
        return False

    def get_group_ids(self):
        repo_group = {}
        for group in self.get("groups"):
            repo_group[group['name']] = group['id']
        return repo_group

    def create_group(self, group_name, visibility="private", request_access_enabled="False"):
        return self.post("groups", {
            "name": group_name,
            "path": group_name,
            "visibility": visibility,
            "request_access_enabled": request_access_enabled
        })

    def get_project(self, project_name, group_id):
        for project in self.get("groups/{}/projects".format(group_id)):
            if project_name == project['name']:
                return project
        return False

    def get_project_ids(self, group_id):
        repo_project = {}
        for project in self.get("groups/{}/projects".format(group_id)):
            repo_project[project['name']] = project['id']
        return repo_project

    def create_project(self, project_name, group_id, visibility="private", request_access_enabled="False"):

        return self.post("projects", {
            "name": project_name,
            "namespace_id": group_id,
            "visibility": visibility,
            "request_access_enabled": request_access_enabled
        })

    def download_project(self, url_repo, dir):
        try:
            git.Repo.clone_from(url_repo, dir)
        except git.GitCommandError as exception:
            print('download project issue', exception)

    def sync(self, path_repo, comment, url_remote):
        project_name = os.path.basename(path_repo)
        repo = git.Repo.init(path_repo)
        res = []
        try:
            repo.create_remote('origin', url=url_remote)
            res.append('Remote associated {}'.format(url_remote))
        except:
            res.append('Remote already associated')

        try:
            repo.remotes.origin.pull('master', allow_unrelated_histories=True)
        except:
            pass

        try:
            repo.git.add(all=True)
            repo.index.commit(comment)
            repo.remotes.origin.push(repo.refs.master)
            res.append('Repo synchronized')
        except:
            res.append('Sync issue')
        return res

    # Human usable function
    def h_list_group(self):
        group_ids = self.get_group_ids()
        for group_name in group_ids:
            project_ids = self.get_project_ids(group_ids[group_name])
            print(group_ids[group_name], group_name, len(project_ids))

    def h_create_group(self, group_name):
        group = self.create_group(group_name)
        if 'id' in group:
            print("Group created", group['id'])
        else:
            print("Group creation issue", group)

    def h_delete_group(self, group_pattern):
        print('Scanning GitLab group...')
        groups = self.get_group_ids()
        for group_name in groups:
            group_id = groups[group_name]
            print(group_name, group_id)
            if group_pattern in group_name:
                projects = self.get_project_ids(group_id)
                for project_name in projects:
                    project_id = projects[project_name]
                    self.delete("projects/{}".format(project_id))
                    print('-', '-', 'Project deleted', project_name, project_id)
                self.delete("groups/{}".format(group_id))
                print('-', 'Group deleted')
            else:
                print('-', 'Group to not delete')
        print('Done')

    def h_list_project(self, group_name=None):
        group_ids = self.get_group_ids()
        for grp_name in group_ids:
            project_ids = self.get_project_ids(group_ids[grp_name])
            if (group_name not in ('', None) and grp_name == group_name) or group_name in ('', None):
                print(group_ids[grp_name], grp_name, len(project_ids))
                for project_name in project_ids:
                    print('  - ', project_ids[project_name], project_name)

    def h_create_project(self, group_name, project_name):
        group = self.get_group(group_name)
        if 'id' not in group:
            group = self.create_group(group_name)
            print("Group created", group['id'])

        project = self.create_project(project_name, group['id'])
        if 'id' in project:
            print("Project created", project['id'])
        else:
            print("Project creation issue", project)

    def h_sync(self, group_prefix, path):
        fl = Filing(path)
        print("Scanning folder", path, '...')
        for group_folder in fl.get_folders(path):
            group_name = '{}{}'.format(group_prefix, os.path.basename(group_folder).lower())

            print(group_name)
            group = self.get_group(group_name)
            if not group:
                group = self.create_group(group_name)
                print('-', "Group Created", group['id'])
            else:
                print('-', "Group already exist", group)

            if 'id' not in group:
                print('-', 'Error', group_name, 'no group id')
            else:
                for project_folder in fl.get_folders(os.path.join(path, group_folder)):
                    project_name = os.path.basename(project_folder)
                    print('-', project_name)

                    project_found = self.get_project(project_name, group['id'])
                    if not project_found:
                        project_found = self.create_project(project_name, group['id'])
                        if 'id' in project_found:
                            print('-', '-', 'Project created', project_found['id'])
                        else:
                            print('-', '-', 'Project updated', project_found)
                    else:
                        print('-', '-', 'Project already exist', project_found)

                    res = self.sync(
                        os.path.join(path, group_folder, project_name),
                        'Auto-commit',
                        self.build_url(group_name, project_name)
                    )
                    for action in res:
                        print('-', '-', '-', action)

    def h_download(self, dir, group_name, project_name=''):

        if project_name not in ('', None) and group_name not in('', None):
            self.download_project(self.build_url(group_name, project_name),
                                  os.path.join(dir, group_name, project_name))
            return

        if group_name not in('', None):
            group = self.get_group(group_name)
            if 'id' not in group:
                print('Group not found', group_name)
            else:
                print('Scanning GitLab project...')
                projects = self.get_project_ids(group['id'])
                for project_name in projects:
                    print("Download project", project_name, projects[project_name])
                    self.download_project(self.build_url(group_name, project_name),
                                          os.path.join(dir, group_name, project_name))
            return

        print('Parameters missing')
