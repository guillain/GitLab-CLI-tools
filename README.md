# GitLab-CLI-tools

Used to synchronize your local folder with your GitLab repositories.

Feature available:
* download all projects from a group
* synchronize all groups and projects (local or remote)
* create, delete, list groups and projects

Requirements:
* python 36 (as only validate on this version)
* gitlab repository (accessible via the network)

## Installation
Clone the repository
`git clone https://github.com/guillain/GitLab-CLI-tools.git`

Move in the folder
`cd GitLab-CLI-tools`

Install the requirements
`pip install -r requirements.txt`

Execute the main script
`python main.py -h`

## Parameters
```
python main.py -a <action> -t <token> [-i <gitlab_url>]
    - action:
        sync
        download
        list_group
        delete_group
        create_group
        list_project
        create_project
    - token: git lab user token (get from your gitlab profile)
    Optional parameters:
        - gitlab_url: default is gitlab.com
        - gitlab_api_path: default is 4
```

## Folder vs Project/Group structure
The folder structure follow the Gitlab and its groups structure.
Each project are uploaded, download or synchronized via the same
template:

**0/ dir parameter = root level**

If you use the *dir* parameter, it will be used as the root level of
the folder management (create, delete, sync, download...)

**1/ group name = first folder level**

The *sync* action can be use with a prefix for the group name
to be sure it will be uniq during the creation (if required).

**2/ project name = second folder level**


## Example
List all groups
`python.exe main.py -a list_groups -t MyToken -w gitlab.guillain.com`

List all projects of a group
`python.exe main.py -a list_project -t MyToken -w gitlab.guillain.com -g MyGroup`

List all projects for all groups
`python.exe main.py -a list_project -t MyToken -w gitlab.guillain.com`

Download
`python.exe main.py -a download -t MyToken -w gitlab.guillain.com -u guillain -g MyGroup -d MyOutpoutFolder`

Synchronize the local folders
`python.exe main.py -a sync -t MyToken -w gitlab.guillain.com -u guillain -d MyInpoutFolder -p "MyGroup-"`
