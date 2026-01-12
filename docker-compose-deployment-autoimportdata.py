compose_dict = {}

compose_scrape = null
compose_validation = null
container_start = null
deployment_check = null

def main():
    compose_collect()
    compose_validate()
    compose_deploy()
    postdeploy_check()

main()