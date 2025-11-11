import re
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.necessary_generic_utils import server_list, scroll_and_click_country, scroll_and_click_server, \
    scroll_and_collect_all_servers, scroll_and_collect_elements_countries
from utils.report_generator import load_countries_and_servers, save_to_csv
from utils.driver_setup import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC







#From the home page after connection collects the server name , ip and other information
def homepage_info(driver):
    """Extract server name, IP, and data usage from the homepage after VPN connection."""
    wait = WebDriverWait(driver, 5)
    server_name = ''
    ip_address = ''
    try:
        # Locate all elements with 'Connected' in content-desc
        get_serverinfo = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//android.view.View[contains(@content-desc,"Connected")]')
        ))

        # Process elements to find the first valid one
        for elem in get_serverinfo:
            content_desc = elem.get_attribute("content-desc")
            if content_desc:
                lines = content_desc.split("\n")
                if len(lines) >= 7:
                    server_name = lines[1].strip()  # Clean up any extra whitespace
                    ip_address = lines[2].strip()
                    downloaded = lines[4].strip()
                    uploaded = lines[6].strip()

                    break  # Stop after finding the first valid element

        # Log the values being returned
        print(f"Returning: Server_name={server_name}, ip_address={ip_address}")
        return {"Server_name": server_name, "ip_address": ip_address}

    except TimeoutException:
        print("❌ Timeout: No elements with 'Connected' found within 30 seconds")
    except NoSuchElementException:
        print("❌ No elements with 'Connected' found")
    except Exception as e:
        print(f"❌ Failed to gather information from the home page: {e}")

    # Always return a dictionary, even on failure
    print(f"Returning default: Server_name={server_name}, ip_address={ip_address}")
    return {"Server_name": server_name, "ip_address": ip_address}

# Go to the Server list
def serverlist(driver):
    #print("Now in the server list")
    try:
        wait = WebDriverWait(driver, 60)
        # Find and click on the server list element
        server = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'))
        )
        server.click()
        time.sleep(2)
        return

    except Exception as e:
        print("The server list is not found:", e)



def connect_disconnect_server(driver, server_name):
    wait = WebDriverWait(driver, 10)
    #Connectin with the selected server
    try:
        connect_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_btn.click()
        print("Connect button clicked")
        time.sleep(3)
    except Exception as e:
        print(f"Failed to click Connect button: {e}")
        return False



    try:

        # try:
        #     homepage_info(driver)
        # except Exception as e:
        #     print("Failed to collect HOme page info function")

        # Retry mechanism
        max_attempts = 2
        attempt = 1

        while attempt <= max_attempts:
            try:
               # print("Now in retry mechanism")
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
                    ))
                )
                #print("Before optimization")
                server_optimization(driver)
                disconnect_server(driver)
                #print("After optimization")
                break  # Exit loop if successful
            except TimeoutException as e :
                #print(f"Attempt {attempt} failed: Element not found or timed out")
                if attempt == max_attempts:
                    #print("Max retries reached - Server appears to be already optimized")
                    #Watch the YouTube video
                    #watch_youtube(driver)
                    # Now going for the Server disconnect
                    #print("Go to third party app to check the IP")
                    # Fetch IP Address from IP Info App
                    try:
                        #print("Going for the ip address validation")
                        validate_ip(driver)

                    except Exception as e:
                        print(f"❌ {server_name} - Failed to fetch IP: {e}")
                        #write_ip_to_csv(server_name, "N/A", "N/A", "❌ Server down", "✅ Connected")

                    switch_back_enova(driver)
                    #print("Time to Disconnect the optimized server")
                    disconnect_server(driver)
                    close_connection_report_popup(driver,"from optimized server")
                    return

                attempt += 1
                time.sleep(2)  # Wait before retrying



    except Exception as e :
        print("Checking the server connection with new mechanism")
        return


def validate_ip(driver):
    """Validate the IP address from VPN app against a third-party IP checker app."""
    server_info = homepage_info(driver)
    server_name = server_info.get("Server_name", "")
    ip_address = server_info.get("ip_address", "")

    if not server_name or not ip_address:
        print("❌ Failed to retrieve server name or IP address from VPN app")
        return

    # print(f"Server name: {server_name}")
    # print(f"Server IP: {ip_address}")

    external_ip = get_ip_from_app(driver)
    try:
        if external_ip is None:
            print("❌ No external IP retrieved from third-party app")
            return

        if ip_address == external_ip:
            print(f"✅{ip_address} == {external_ip}, IP matched")
        else:
            print(f"❌{ip_address} != {external_ip}, IP mismatch")
    except Exception as e:
        print(f"❌ Failed to validate IP: {e}")
    return


#Third Party app to check the ip
def get_ip_from_app(driver):
    """ Fetches the public IP using the IP Info App """
    app_package = "cz.webprovider.whatismyipaddress"
    app_activity = "cz.webprovider.whatismyipaddress.MainActivity"

    # Open IP Info App
    driver.execute_script("mobile: shell", {"command": f"am start -n {app_package}/{app_activity}"})
    time.sleep(5)

    try:
        refresh_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/refresh_info"))
        )
        refresh_button.click()
        time.sleep(5)

        ip_element = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/zobraz_ip"))
        )
        print("Ip from the My Ip app : ", ip_element.text.strip())
        return ip_element.text.strip()

    except TimeoutException:
        print("❌ IP fetch timed out.")
        return None

    except NoSuchElementException as e:
        print(f"❌ IP element not found: {e}")
        return None

    finally:
        driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
        #print("📱 Returned to home screen.")

#Switch back to Enova vpn application

def switch_back_enova(driver):

    # Switch back to Enova VPN
    try:
        driver.execute_script("mobile: shell", {"command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"})
        time.sleep(2)
    except Exception as e:
        #print(f"❌ {server_name} - Failed to reopen Enova VPN: {e}")
        return



def disconnect_server(driver):
    wait = WebDriverWait(driver,5)
    # Disconnect the VPN
    try:
        turn_on_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        disconnect_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        time.sleep(3)
        #print(f"🔌 {server_name} disconnected successfully.")
       # print("Disconnected successfully")
        #connection_report(driver)
        return
    except Exception as e:
       # print(f"❌ {server_name} - Disconnection failed: {e}")
        print("Failed to disconnect")
        return






#From the home page after connection collects the server name , ip and other information
def homepage_info(driver):
    wait = WebDriverWait(driver, 5)
    server_name = ''
    ip_address = ''
    try:
        get_serverinfo = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, f'//android.view.View[contains(@content-desc,"Connected")]')
        ))

        for elem in get_serverinfo:
            content_desc = elem.get_attribute("content-desc")
            if content_desc:
                lines = content_desc.split("\n")
                if len(lines) >= 7:
                    server_name = lines[1]
                    ip_address = lines[2]
                    downloaded = lines[4]
                    uploaded = lines[6]
        return {"Server_name": server_name, "ip_address": ip_address}
    except Exception as e:
        print("Failed to gather information from the home page")

    return


def server_optimization(driver):
    """ Handle server optimization popup """
    #print("Now in the server optimization Function")
    wait = WebDriverWait(driver, 5)

    optimization_msg = wait.until(EC.presence_of_element_located((
        By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
    )))

    #print("Now in the server optimization Function")
    wait = WebDriverWait(driver, 5)

    full_text = optimization_msg.get_attribute("content-desc")
    print("Full text:", full_text)

    match = re.search(r"Unfortunately,\s*(.*?)\s*is not optimized", full_text)
    server_name = match.group(1).strip() if match else None
    if server_name:
        print("Server name:", server_name)
    else:
        print("No server name found")


    close_connection_report_popup(driver,"not optimed")
    return server_name





def close_connection_report_popup(driver,value):
    print(value)
    wait=WebDriverWait(driver,5)
    try:

        get_popup = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.widget.ImageView[1]'
        )))
        get_popup.click()
        #print("✅ Popup closed successfully.")
    except Exception as e:
        print("⚠️ Failed to close popup")

    return


def server_check(driver):


    # Example usage:
    countries1, servers1 = load_countries_and_servers("collected_countries_servers.csv")
    print("✅ Countries:", countries1)
    print("✅ Servers:", servers1)

    for server in servers1:
        server_list(driver)
        matched_country = None
        server = server.strip()
        print(f"Checking server: {server}")

        for country in countries1:
            if server.lower().startswith(country.lower()):
                matched_country = country
                break

        if matched_country:
            print(f"🌍 Server '{server}' belongs to country '{matched_country}'")
            scroll_and_click_country(driver, matched_country)
            scroll_and_click_server(driver, server)
        else:
            print(f"⚡ Server '{server}' not tied to any country — searching directly")
            scroll_and_click_server(driver, server)

        # Connect/disconnect each server **inside the loop**
        connect_disconnect_server(driver, server)



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


# --- Main Entry ---
def main():
    driver = setup_driver()
    #collecting_servers_name(driver)
    #driver.quit()
    server_check(driver)



if __name__ == "__main__":
    main()