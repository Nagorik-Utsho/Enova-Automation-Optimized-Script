import time


from utils.driver_setup import *
from utils.helpers import wait_and_click
from utils.locators import *
from utils.necessary_generic_utils import *
from utils.report_generator import save_to_csv, load_countries_and_servers

countries = set()
servers = set()

def collect_countries_servers(driver):




    result=scroll_and_collect_elements_countries(driver)
    print(result)

    for item in result['elements']:
        if '-' in item :
            servers.add(item)
        else :
            countries.add(item)

    countries.remove("Brazil")
    servers.add("Brazil")
    print(f"Collected countries name :{countries}")

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


def collecting_servers_name(driver):

    server_list(driver)
    time.sleep(3)
    collect_countries_servers(driver)
    save_to_csv(countries, servers, "collected_countries_servers.csv")


def time_to_click(driver):

    server_list(driver)
    print("After Reading from the csv")

    # Example usage:
    countries1, servers1 = load_countries_and_servers("collected_countries_servers.csv")
    print("✅ Countries:", countries1)
    print("✅ Servers:", servers1)

    for server in servers1:
        matched_country = None

        print(f"Random countries name: {server} ")
        # 🔹 Check if any country name is part of the server name
        for country in countries1:
            if server.lower().startswith(country.lower()):
                matched_country = country
                break

        if matched_country:
            print(f"🌍 Server '{server}' belongs to country '{matched_country}'")
            scroll_and_click_country(driver, matched_country)
            scroll_and_click_server(driver, server)  # Then click the server
        else:
            print(f"⚡ Server '{server}' not tied to any country — searching directly")
            scroll_and_click_server(driver, server)









# --- Main Entry ---
def main():
    driver = setup_driver()
    #collecting_servers_name(driver)
    #driver.quit()
    print(" Time to click on the server list ")
    time_to_click(driver)


if __name__ == "__main__":
    main()