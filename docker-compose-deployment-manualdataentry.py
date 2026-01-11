import os
import subprocess
import urllib
import requests
from time import sleep

compose_dict = {}

def compose_collect(compose_dict):

    # This function serves the purpose of collecting data on the containers/applications to be deployed. 
    # It loops through the collection process in the case that the user wants to deploy multiple containers at once.
    
    additional_deployment = None

    while additional_deployment != "N":
        application_name = input("Name of the container being deployed: ")
        compose_location = input("Absolute path or URL for your compose file: ").strip()
        deployment_location = input("Deployment directory for this container: ")
    
        # The below if statement checks whether the directory exists and creates it if it doesn't. 
        # Chose to create this as if the user will always want to create the directory if it does not already exist.

        if not os.path.exists(deployment_location):        
            try:
                subprocess.run(
                    ["mkdir", "-p", deployment_location], 
                    check=True
                )
                print(f"Successfully generated missing deployment directory: {deployment_location}.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to create directory: {e}")
                exit()
    
        compose_dict[application_name] = {
            "application_name" : application_name,
            "compose_location" : compose_location,
            "deployment_directory" : deployment_location
        }
        additional_deployment = input("Would you like to deploy an additional container (Y/N)?: ").strip().upper()
    return compose_dict

def compose_process(compose_dict):

    # This function iterates through the compose_dict dictionary to grab the desired deployment locations for the containers.
    # It then parses the locations, pulls the compose file if the location is one, and then proceeds to place the compose files into the related deployment directory.

    for application_name, details in compose_dict.items():
        application_name = details["application_name"]
        compose_location = details["compose_location"]
        deployment_directory = details["deployment_directory"]

        if urllib.parse.urlparse(compose_location).scheme:
            print(f"Downloading remote {application_name} compose file and placing in deployment directory...")
            try:
                response = requests.get(compose_location)
                response.raise_for_status()  # Raises an error for bad responses
                with open(os.path.join(deployment_directory, "docker-compose.yml"), "wb") as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                print(f"Failed to place {application_name} compose file: {e}")
                continue

        else:
            try:
                print(f"Copying local {application_name} compose file to it's deployment directory...")
                subprocess.run(
                ["cp", compose_location, os.path.join(deployment_directory, "docker-compose.yml")], 
                check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Failed to copy {application_name} compose file to {deployment_directory}: {e}")
                continue

def compose_deploy(compose_dict):

    # This function will iterate through the deployment location value(s) and deploy all specified containers/applications.

    input("Configure your compose files if necessary and then press enter to continue.")

    for application_name, details in compose_dict.items():
        deployment_directory = details["deployment_directory"]
        try:
            subprocess.run(
            ["docker", "compose", "up", "-d"], 
            cwd=deployment_directory,
            check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Your container failed to deploy: {e}")

def deployment_check(compose_dict):

    # This function performs a post deployment check and prints out the result.
    # I would like to find a way to order these based on their state but for now will work to get it functioning without a specific order.

    print("Waiting for containers to start. Please do not escape the script.")
    time.sleep(30)
    
    for application_name, details in compose_dict.items():
        application_name = details["application_name"]
        try:
            get_status = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Status}}", application_name], 
                capture_output=True, 
                text=True, 
                check=True
                )
            print(f"The container {application_name} output a status of {get_status.stdout.strip()}")
        except subprocess.CalledProcessError as e:    
            print(f"Unable to get status of container {application_name}. Error: {e}")

def main():
    compose_collect(compose_dict)
    compose_process(compose_dict)
    compose_deploy(compose_dict)
    deployment_check(compose_dict)

main()
