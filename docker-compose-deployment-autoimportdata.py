compose_dict = {}

compose_scrape = null
compose_validation = null
container_start = null
deployment_check = null

def main():
    compose_scrape()
    compose_validation()
    container_start()
    deployment_check()

main()