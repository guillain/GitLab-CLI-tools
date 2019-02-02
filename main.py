#!/usr/bin/python
import os
import sys
import getopt
from classes.gitlab import Gitlab

debug = False
default_git_url = "gitlab.com"
default_git_version = "4"

def help_me():
    print('python main.py -a <action> -t <token> [-i <gitlab_url>]')
    print('- action: sync, download, list_group, delete_group, create_group, list_project, create_project')
    print('- token: git lab user token (get from your gitlab profile)')
    print('Optional parameters:')
    print('- gitlab_url: default is ' + default_git_url)
    print('- gitlab_api_path: default is ' + default_git_version)
    print('Depend on of your action, specific parameters can be required')


def exit(help=None, level=None):
    if help:
        help_me()
    sys.exit(level)


def main(argv):
    # Init parameters
    action = ''
    token = ''
    user = ''
    dir = ''
    prefix = ''
    group_name = ''
    project_name = ''
    git_url = default_git_url
    git_version = default_git_version

    # Get parameters from CLI
    try:
        opts, args = getopt.getopt(argv,
                                   "ha:t:u:d:f:g:p:r:w:v:",
                                   ["help", "action=", "token=", "user=", "dir=", "prefix=",
                                    "group_name=", "project_name=", "git_url=", "git_version="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                exit('help')
            elif opt in ("-a", "--action"):
                action = arg
            elif opt in ("-t", "--token"):
                token = arg
            elif opt in ("-u", "--user"):
                user = arg
            elif opt in ("-d", "--dir"):
                dir = arg
            elif opt in ("-f", "--prefix"):
                prefix = arg
            elif opt in ("-g", "--group_name"):
                group_name = arg
            elif opt in ("-p", "--project_name"):
                project_name = arg
            elif opt in ("-w", "--git_url"):
                git_url = arg
            elif opt in ("-v", "--git_version"):
                git_version = arg
    except getopt.GetoptError:
        print("Get parameter parsing error")
        exit('help', 2)

    # Check parameters
    if token in ('', None):
        print('No token provided')
        exit("help", 1)

    if action in ('', None):
        print('No action provided')
        exit("help", 1)

    # Print debug
    if debug:
        print('Action: ', action)
        print('Token: ', token)
        print('User: ', user)
        print('Dir: ', dir)
        print('Prefix: ', prefix)
        print('Group_name: ', group_name)
        print('Project_name: ', project_name)
        print('Git url: ', git_url)
        print('Git version: ', git_version)

    # Init Gitlab object
    gl = Gitlab(token=token, url=git_url, version=git_version, user=user)

    # Execute the requested action
    if action == 'delete_group':
        if prefix in ('', None):
            print('Thanks to provide also the prefix of the gitlab group to delete')
            print('- The gitlab group prefix to delete: -g "tonton-" / --group_prefix "tonton-" / group_prefix="tonton-"')
            exit("help", 1)
        gl.h_delete_group(prefix)

    elif action == 'sync':
        if user in ('', None) or prefix in ('', None) or dir in ('', None):
            print('Thanks to provide also the following mandatory parameters:')
            print('- The gitlab user name: -u "tonton" / --user "tonton" / user="tonton"')
            print('- The gitlab group prefix to add for gorup creation: -p "tonton-" / --prefix "tonton-" / prefix="tonton-"')
            print('- The path of the folder structure to analyze: -d "./dev" / --dir "./dev" / dir="./dev"')
            exit("help", 1)
        gl.h_sync(token, user, prefix, dir)

    elif action == 'download':
        if user in ('', None) or dir in ('', None) or group_name in ('', None):
            print('Thanks to provide also the following mandatory parameters:')
            print('- The gitlab user name: -u "tonton" / --user "tonton" / user="tonton"')
            print('- The folder where to store the download: -d "./dev" / --dir "./dev" / dir="./dev"')
            print('- The gitlab group name: -g "tonton-python" / --group_name "tonton-python" / group_name="tonton-python"')
            print('Optionnaly if it\'s only the project to download')
            print('- The gitlab project name: -p "gitlab-mirroring" / --project_name "gitlab-miroring" / project_name="gitlab-mirroring"')
            exit("help", 1)
        gl.h_download(dir, group_name, project_name)

    elif action == 'list_group':
        gl.h_list_group()

    elif action == 'create_group':
        if group_name in ('', None):
            print('Thanks to provide also the group name to create:')
            print('- The gitlab group name: -g "tonton-python" / --group_name "tonton-python" / group_name="tonton-python"')
            exit("help", 1)
        gl.h_create_group(group_name)

    elif action == 'list_project':
        gl.h_list_project(group_name)

    elif action == 'create_project':
        if project_name in ('', None) or group_name in ('', None):
            print('Thanks to provide also the group name (created if not exist) and the project name:')
            print('- The gitlab user name: -n "tonton" / --name "tonton" / name="tonton"')
            print('- The gitlab group name: -g "tonton-python" / --group_name "tonton-python" / group_name="tonton-python"')
            exit("help", 1)
        gl.h_create_project(group_name, project_name)

    else:
        print('action not found')
        exit('help', 2)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('No parameters provided')
        exit("help", 2)
    main(sys.argv[1:])
