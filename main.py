
from WireGuard.WireGuard_Protocol_testing import *


def main():
    driver = setup_driver()
    #wireguard_servers(driver)
    wireguard_protocol_testing(driver)



if __name__ == "__main__":
    main()
