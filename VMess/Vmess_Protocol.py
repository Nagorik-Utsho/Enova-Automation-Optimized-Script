import re
from logging import exception

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
def setup_driver():

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "12"
    options.device_name = "10ECBH02JJ000D2"
    options.app_package = "com.enovavpn.mobile"
    options.app_activity = "com.enovavpn.mobile.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    options.new_command_timeout = 300
    options.auto_grant_permissions = True
    options.ensure_webviews_have_pages = True
    options.dont_stop_app_on_reset = True
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    return driver

def scroll_and_click_in_scrollview_server_name(driver, element_text,
                                   scrollview_xpath='//android.widget.ScrollView',

                                   max_scrolls_per_direction=10, max_cycles=10):
    """
    Scrolls inside a ScrollView container to find an element by accessibility id (content-desc) and clicks it.
    Strategy:
        - Scroll down fully (up to max_scrolls_per_direction times).
        - If not found, scroll up fully.
        - Repeat this cycle up to max_cycles times.
    """

    try:
        # Wait up to 120 seconds for the scrollable container
        wait = WebDriverWait(driver, 5)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found within 120 seconds.")
        return False

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        #print(f"🔄 Starting cycle {cycle + 1}/{max_cycles}...")

        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    # Always re-fetch the ScrollView to avoid stale references
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

                    try:
                        #element = scrollable.find_element(AppiumBy.ACCESSIBILITY_ID, element_text)
                        element = scrollable.find_element(
                            AppiumBy.XPATH,
                            f'.//*[self::android.view.View or self::android.widget.ImageView][contains(@content-desc, "{element_text}")]'
                        )

                        element.click()
                        #print(f"✅ Found and clicked element: {element_text}")
                        return True
                    except NoSuchElementException:
                       # print(f"➡️ Scrolling {direction} (attempt {attempt + 1}/{max_scrolls_per_direction})")
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.2
                        })
                        time.sleep(0.5)

                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '{element_text}' not found after {max_cycles} cycles "
          f"(down+up, {max_scrolls_per_direction} each).")
    return False


#New scrolling mechanism
def scroll_and_click_in_scrollview(driver, element_text,
                                   scrollview_xpath='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[5]/android.view.View/android.view.View/android.view.View',

                                   max_scrolls_per_direction=10, max_cycles=10):
    """
    Scrolls inside a ScrollView container to find an element by accessibility id (content-desc) and clicks it.
    Strategy:
        - Scroll down fully (up to max_scrolls_per_direction times).
        - If not found, scroll up fully.
        - Repeat this cycle up to max_cycles times.
    """

    try:
        # Wait up to 120 seconds for the scrollable container
        wait = WebDriverWait(driver, 5)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found within 120 seconds.")
        return False

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        #print(f"🔄 Starting cycle {cycle + 1}/{max_cycles}...")

        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    # Always re-fetch the ScrollView to avoid stale references
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

                    try:
                        #element = scrollable.find_element(AppiumBy.ACCESSIBILITY_ID, element_text)
                        element = scrollable.find_element(
                            AppiumBy.XPATH,
                            f'.//*[self::android.view.View or self::android.widget.ImageView][contains(@content-desc, "{element_text}")]'
                        )

                        element.click()
                        #print(f"✅ Found and clicked element: {element_text}")
                        return True
                    except NoSuchElementException:
                       # print(f"➡️ Scrolling {direction} (attempt {attempt + 1}/{max_scrolls_per_direction})")
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.6
                        })
                        time.sleep(0.5)

                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '{element_text}' not found after {max_cycles} cycles "
          f"(down+up, {max_scrolls_per_direction} each).")
    return False


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
                    #print(f"Server Name: {server_name}")
                    #print(f"IP Address: {ip_address}")
                    #print(f"Downloaded: {downloaded}")
                    #print(f"Uploaded: {uploaded}")
                    #print("---")  # Separator for clarity
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
    """Connect to VPN server, optimize it, validate IP and disconnect."""
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(3)

    print(f"\nAttempting to connect to {server_name}...")
    wait = WebDriverWait(driver, 10)

    # Open server list
    serverlist(driver)

    # -------------------------------------------------
    # 1. Expand country dropdowns
    # -------------------------------------------------
    countries_to_expand = ["France", "Germany", "United Kingdom", "United States", "Japan", "Canada"]
    target_country = next((c for c in countries_to_expand if c in server_name), None)

    if not target_country:
        print(f"Country not recognized in server name: {server_name}")
        return False

    print(f"Target country: {target_country}")

    expanded = False
    for country in countries_to_expand:
        if country == target_country or country in server_name:
            print(f"Expanding country: {country}")
            if scroll_and_click_in_scrollview(driver, country):
                expanded = True
                time.sleep(1)

    if not expanded:
        print("None of the expected countries could be expanded.")
        return False

    # -------------------------------------------------
    # 2. Click the exact server
    # -------------------------------------------------
    time.sleep(2)  # wait for server list to load
    if not scroll_and_click_in_scrollview(driver, server_name):
        print(f"Target server '{server_name}' not found.")
        return False

    print(f"Successfully selected server: {server_name}")

    # -------------------------------------------------
    # 3. Choose security layer (VLess → Smart)
    # -------------------------------------------------
    vless_xpath = '//android.view.View[contains(@content-desc,"VLess")]'
    smart_xpath = '//android.view.View[contains(@content-desc,"Smart")]'

    try:
        print("Selecting security layer...")
        select_vless = wait.until(EC.element_to_be_clickable((By.XPATH, vless_xpath)))
        select_vless.click()
    except Exception:
        try:
            select_smart = wait.until(EC.element_to_be_clickable((By.XPATH, smart_xpath)))
            select_smart.click()
        except Exception:
            print("Failed to select any security layer (VLess/Smart)")

    # -------------------------------------------------
    # 4. Click Connect button
    # -------------------------------------------------
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

    # -------------------------------------------------
    # 5. Optimization + retry logic
    # -------------------------------------------------
    max_attempts = 2
    optimized = False

    for attempt in range(1, max_attempts + 1):
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
                ))
            )
            print("Running optimization...")
            server_optimization(driver)
            optimized = True
            break
        except TimeoutException:
            print(f"Attempt {attempt}/{max_attempts}: Already optimized or element not found")
            if attempt == max_attempts:
                optimized = True   # treat as already optimized
            time.sleep(2)

    # -------------------------------------------------
    # 6. IP validation (third-party app)
    # -------------------------------------------------
    try:
        print("Validating IP address...")
        validate_ip(driver)
    except Exception as e:
        print(f"IP validation failed: {e}")

    # -------------------------------------------------
    # 7. Switch back to Enova & disconnect
    # -------------------------------------------------
    switch_back_enova(driver)
    disconnect_server(driver)
    close_connection_report_popup(driver, "from optimized server")

    print(f"{server_name} – flow completed.")
    return True


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



# def connection_report(driver,server_name) :
#     wait=WebDriverWait(driver,5)
#     # Define labels
#     labels = [
#         "Server Name",
#         "IP Name",
#         "Connection Duration",
#         "Upload Time",
#         "Download Time"
#     ]
#
#     print("------ Connection Info ------")
#
#     try:
#         print(f"Disconnection pop up is present for{server_name}")
#         # Get all android.view.View elements with content-desc
#         all_elements = wait.until(EC.presence_of_all_elements_located(
#             (By.XPATH, '//android.view.View[@content-desc]')
#         ))
#
#         # Skip first two irrelevant elements
#         relevant_elements = all_elements[2:]  # Starts from 3rd element
#
#         for i, label in enumerate(labels):
#             value = relevant_elements[i].get_attribute("content-desc") if i < len(relevant_elements) else "None"
#             print(f"{label}: {value}")
#
#     except Exception:
#          print(f"Disconnection pop up is not present for {server_name}")
#         # If elements not found
#         for label in labels:
#             print(f"{label}: None")
#
#     return

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



                    #print("---")  # Separator for multiple entries

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
    print("##### Server Status Check #######")
    servers = ["India - 2","India - 4","India - 3","India - Premium",
                "USA - 4","USA - Premium","USA - Super",
               "France - 6","France - 4","France - 5","France - Special","France - Warrior", "France - Premium"
               "Netherlands - 1","Brazil","Singapore - 1",
               "Germany - 6","Germany - 10","Germany - 11",
               "Canada - 2", "Poland Premium"
               ]

    # Define countries and servers
    countries = ["India", "USA", "France","Germany"]
    server_country_map = {}

    for server in servers:
        matched_country = None
        for country in countries:
            # Match server start or contains (for flexible names)
            if server.startswith(country):
                matched_country = country
                break
        # If not matched, assume the server itself is the country
        if matched_country is None:
            matched_country = server.split(" - ")[0] if " - " in server else server
        server_country_map[server] = matched_country




    for server, country in server_country_map.items():
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        time.sleep(5)
        connect_disconnect_server(driver, country, server)

        # Pass both country and server name



# --- Main Entry ---
def main():
    driver = setup_driver()
    server_check(driver)
    driver.quit()


if __name__ == "__main__":
    main()