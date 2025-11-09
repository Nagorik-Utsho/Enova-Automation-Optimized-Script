import time

from utils.driver_setup import *
from utils.helpers import wait_and_click
from utils.locators import *
from utils.necessary_generic_utils import *

countries = set()
servers = set()

def go_to_premium_tab(driver):


    #wait_and_click(driver,location_type.premium_xpath)

    result=scroll_and_collect_elements_countries(driver)
    print(result)

    for item in result['elements']:
        if '-' in item :
            servers.add(item)
        else :
            countries.add(item)

    countries.remove("Brazil")
    servers.add("Brazil")
    print(countries)
    print(servers)

    for country in countries :
        #xpath = CountryDropdown.close_dropdown(country)
        print(f"Trying  to click:{country}")
        scroll_and_click_country(driver,country)

        all_servers=scroll_and_collect_all_servers(driver)

        for premium_server in all_servers['elements'] :
            servers.add(premium_server)

        # Step 2: Wait for it and click
        #wait_and_click(driver, xpath)
        #time.sleep(.2)





    print(servers)
    print(f'Total number of server :{len(servers)} ')








# --- Main Entry ---
def main():
    driver = setup_driver()
    time.sleep(3)
    server_list(driver)
    time.sleep(3)
    go_to_premium_tab(driver)


if __name__ == "__main__":
    main()