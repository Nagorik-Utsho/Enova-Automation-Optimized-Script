from utils.driver_setup import setup_driver
from utils.servers_util import *


def main():
    driver = setup_driver()
    wireguard_servers(driver)


if __name__ == "__main__":
    main()
