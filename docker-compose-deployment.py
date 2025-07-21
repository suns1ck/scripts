import os
import subprocess
import urllib
import requests

compose_dict = {}

def compose_collect(compose_dict):

    # This function serves the purpose of collecting data on the containers/applications to be deployed. It loops through the collection process
    # in the case that the user wants to deploy multiple containers at once.
    
    additional_deployment = None

    while additional_deployment != "N":
        application_name = input("Name of the application being deployed: ")
        compose_location = input("Absolute path or URL for your compose file: ").strip()
        deployment_location = input("Deployment directory for this container/application: ")
    
        # The below if statement checks if the directory exists and creates it if desired. Chose to create this as if the user will always want
        # to create the directory if it does not already exist.

        if not os.path.exists(deployment_location):        
            try:
                subprocess.run(["mkdir", "-p", deployment_location], check=True)
                print(f"Successfully created directory ({deployment_location})")
            except subprocess.CalledProcessError as e:
                print(f"Failed to create directory: {e}")
                exit()
    
        compose_dict[application_name] = {
            "application_name" : application_name,
            "compose_location" : compose_location,
            "deployment_directory" : deployment_location
        }
        additional_deployment = input("Would you like to deploy an additional container/application (Y/N)?: ").strip().upper()
    return compose_dict

def compose_process(compose_dict):

    # This function iterates through the compose_dict dictionary to grab the locations of the declared containers/applications.
    # It then parses the locations, pulls the compose file if the location is one, and then proceeds to place the compose file(s)
    # into the related deployment directory.

    for application_name, details in compose_dict.items():
        application_name = details["application_name"]
        compose_location = details["compose_location"]
        deployment_directory = details["deployment_directory"]

        if urllib.parse.urlparse(compose_location).scheme:
            print(f"Downloading remote compose file for {application_name} and placing in deployment directory.")
            try:
                response = requests.get(compose_location)
                response.raise_for_status()  # Raise an error for bad responses
                with open(os.path.join(deployment_directory, "docker-compose.yml"), "wb") as f:
                    f.write(response.content)
                print(f"Successfully placed {application_name} compose file.")
            except requests.exceptions.RequestException as e:
                print(f"Failed to place {application_name} compose file: {e}")
                continue

        else:
            try:
                print(f"Copying local compose file for {application_name} to it's deployment directory.")
                subprocess.run(["cp", compose_location, os.path.join(deployment_directory, "docker-compose.yml")], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to copy {application_name} compose file to {deployment_directory}: {e}")
                continue

def compose_deploy(compose_dict):

    # This function will iterate through the deployment location value(s) and deploy all specified containers/applications.

    for application_name, details in compose_dict.items():
        deployment_directory = details["deployment_directory"]

        try:
            subprocess.run(["docker-compose", "up", "-d"], cwd=deployment_directory, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Your container failed to deploy: {e}")


compose_collect(compose_dict)
compose_process(compose_dict)
compose_deploy(compose_dict)