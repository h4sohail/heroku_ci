import requests
import json, time, os, subprocess, datetime
from shutil import copyfile, rmtree

heroku_app_name = 'Heroku-App-Name' # Heroku app name (get it from Heroku dashboard)

github_username = 'johndoe' # GitHub username
github_repo_name = 'cool-repo' # GitHub repo name
github_repo_clone_url = 'https://github.com/johndoe/cool-repo.git' # GitHub repo url
github_token = 'GitHub-Personal-Access-Token' # https://github.com/settings/tokens

url = f'https://api.github.com/repos/{github_username}/{github_repo_name}'
params = {'access_token': github_token}

response = requests.get(url, params = params)

if response:
    data = json.loads(response.content)
    initial_time_stamp = (data["updated_at"]) # Check when the repository was last updated
else:
    print('Something went wrong :)')

exit_condition = True        
while(exit_condition):
    response = requests.get(url, params = params)
    if response:
        data = json.loads(response.content)
        current_time_stamp = (data["updated_at"])  # Re-check every 5 seconds for when the repository was updated
        
        if initial_time_stamp != current_time_stamp: # Check if the two timestamps are not equal
            initial_time_stamp = current_time_stamp
            print('Change Detected')
            try:
                if os.path.exists(f'/home/ubuntu/code/heroku_ci/projects/{github_repo_name}'):
                    rmtree(f'/home/ubuntu/code/heroku_ci/projects/{github_repo_name}') # Delete the old files
                    print('Deleted old files')
            except OSError as identifier:
                print(identifier)
            
            try:
                os.chdir('/home/ubuntu/code/heroku_ci/projects')
                os.system(f'git clone {github_repo_clone_url}') # Clone the files
                print('Cloned new files')
            except OSError as identifier:
                print(identifier) 
            
            try:
                os.chdir(f'/home/ubuntu/code/heroku_ci/projects/{github_repo_name}') 
                print(f'Changed directory to {github_repo_name}') # Change the directory
            except OSError as identifier:
                print(identifier) 
            
            try:
                os.system(f'heroku git:remote -a {heroku_app_name}') # Add Heroku remote
                print(f'Added heroku remote')
            except OSError as identifier:
                print(identifier)

            try:
                os.system(f'git pull heroku master') # Grab necessary files form Heroku
                print(f'Got necessary files from heroku')
            except OSError as identifier:
                print(identifier)
            
            try:
                os.system('git push heroku master') # Push to Heroku
                print('Updated Heroku')
            except OSError as identifier:
                print(identifier)
        
        print(datetime.datetime.now(), 'No changes')
        time.sleep(5)

    else:
        print('Something went wrong :)')
        exit_condition = False