import os
import subprocess

compose_dict = {}

def compose_collect(compose_dict):

    # This function requests the compose file location from the user, collects the contained data, and places it into compose_dict.

    additional_deployment = None

    while additional_deployment != 'N':
        compose_location = input("Please enter the full path to your docker compose file (/dir/compose.yml): ").strip()

        if os.path.exists(compose_location):
            try:
                with open(compose_location, 'r') as compose:
                    None
            except:
                None
        if not os.path.exists(compose_location):
            print("The specified file does not exist. Check everything is in order and try again.")

compose_validation = None
container_start = None
deployment_check = None

def main():
    compose_collect()
    compose_validate()
    compose_deploy()
    postdeploy_check()

main()