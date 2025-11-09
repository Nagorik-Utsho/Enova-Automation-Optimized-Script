import re
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
    options.platform_version = "15"
    options.device_name = "R4BW600110K"
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

def scroll_and_click_in_scrollview1(driver, element_text,
                                       scrollview_xpath="//android.widget.ScrollView",
                                       max_scrolls_per_direction=10,
                                       max_cycles=3):
        """
        Improved scroll and click mechanism for ScrollView-based layouts.
        Fixes issues where elements are skipped or not clickable
        due to rendering lag or blind scrolling.

        Strategy:
            - Alternate between downward and upward scrolling.
            - After each scroll, re-check for element multiple times.
            - Auto-stop once found.
        """

        wait = WebDriverWait(driver, 5)
        try:
            scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
        except TimeoutException:
            print("❌ ScrollView container not found.")
            return False

        directions = ["down", "up"]

        for cycle in range(max_cycles):
            for direction in directions:
                for attempt in range(max_scrolls_per_direction):
                    # Refresh scrollable every time to avoid stale refs
                    try:
                        scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)
                    except StaleElementReferenceException:
                        print("⚠️ ScrollView went stale, retrying...")
                        continue

                    # Try to find the target element (with small waits)
                    for retry in range(3):  # retry visibility check 3x
                        try:
                            element = scrollable.find_element(
                                AppiumBy.XPATH,
                                f'.//*[contains(@content-desc, "{element_text}")]'
                            )
                            # Additional check: ensure element is visible
                            if element.is_displayed():
                                element.click()
                                print(
                                    f"✅ Found and clicked '{element_text}' (cycle {cycle + 1}, attempt {attempt + 1})")
                                return True
                        except NoSuchElementException:
                            pass
                        time.sleep(0.5)  # small delay to let UI render

                    # Scroll if not found
                    try:
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.3  # smaller scroll step = less overshoot
                        })
                    except Exception as e:
                        print("⚠️ Scroll gesture failed:", e)
                        continue

                    time.sleep(0.8)  # small pause after each scroll

        print(f"❌ Element '{element_text}' not found after full scroll in both directions.")
        return False

    #New scrolling mechanism
def scroll_and_click_in_scrollview(driver, element_text, max_scrolls_per_direction=4, max_cycles=3):
    """
    Generic scroll-and-click for dynamic Android layouts.
    Automatically detects scrollable containers and scrolls smoothly.
    """

    print(f"🔍 Searching for element: {element_text}")

    # Wait for at least one scrollable container to appear
    try:
        WebDriverWait(driver, 20).until(
            lambda d: len(d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().scrollable(true)')) > 0
        )
    except TimeoutException:
        return {"status": "FAILED", "message": "No scrollable container found"}

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        scrollables = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().scrollable(true)'
        )

        if not scrollables:
            print("⚠️ No scrollable containers detected.")
            return {"status": "FAILED", "message": "No scrollables found"}

        # Always target the last (most recent) scrollable container
        scrollable = scrollables[-1]

        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    # Try finding the element in current view
                    element = driver.find_element(
                        AppiumBy.XPATH,
                        f'//*[contains(@content-desc, "{element_text}")]'
                    )
                    element.click()
                    print(f"✅ Clicked '{element_text}' successfully")
                    return {"status": "SUCCESS", "message": f"Clicked {element_text}"}
                except NoSuchElementException:
                    # Smooth scroll using mobile gesture
                    try:
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.6,
                            "speed": 600  # smoother, slightly slower scroll
                        })
                        time.sleep(0.4)
                    except Exception as inner_e:
                        print(f"⚠️ Scroll attempt failed: {inner_e}")
                except StaleElementReferenceException:
                    print("♻️ Scrollable element went stale, re-locating...")
                    break

    print(f"❌ Element '{element_text}' not found after scrolling.")
    return {"status": "FAILED", "message": f"Element '{element_text}' not found"}



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
    """ Connect to VPN server and run optimization """
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(3)

    print(f"\n🚀 Attempting to connect to {server_name}...")
    wait = WebDriverWait(driver, 10)
    # Open server
    serverlist(driver)

    countries = ["France"]
    if "France" in server_name:
        # Opening the country drop down
        try:
            # 🔽 Expand all available countries (first pass)

            for country in countries:
                # print(f"🔍 Looking for {country}...")
                if not scroll_and_click_in_scrollview(driver, country):
                    print(f"❌ Country '{country}' not found in list.")
                    return
        except Exception as e:
            print("ALL the drop_down are opened")

    #Selecting the server name
    try :
        # print(f"🔎 Searching for target server: {server_name}...")
        if not scroll_and_click_in_scrollview(driver, server_name):
            print(f"❌ Target server '{server_name}' not found, skipping connection.")
            return
    except Exception as e :
        print(f"{server_name} not found")


    #Connectin with the selected server
    try :
        #Connect the server
        # Click Connect
        connect_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_button.click()
        time.sleep(.3)
    except Exception as e :
        print ("Failed to connect with the server")



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
                    #print(f"Server Name: {server_name}")
                    #print(f"IP Address: {ip_address}")
                    #print(f"Downloaded: {downloaded}")
                    #print(f"Uploaded: {uploaded}")



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
    servers = ['India - 3','Netherlands - 1','Brazil',
               "Singapore - 1","Japan",
               "France - 4","France  Warrior"
               ,"Germany - 6","USA - 1","Italy - Premium"]


    for server in servers:
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        time.sleep(0.5)
        connect_disconnect_server(driver, server)
        #print("now go for sleeping mode")




# --- Main Entry ---
def main():
    driver = setup_driver()
    server_check(driver)
    driver.quit()


if __name__ == "__main__":
    main()


    servers = [ "Denmark - Warrior" , "Turkey - 2" , "Poland Premium" ,  "Canada - 2",
                "Indonesia" , "Japan" , "Italy - Premium " ,"Netherlands - 1","Brazil",
                "India - 2","India - 4","India - 3","India - Premium",
                "USA - 1","USA - 4","USA - Premium","USA - Super",
               "France - 6","France - 4","France - 5","France - Special","France - Warrior", "France - Premium"
               "Singapore - 1","Singapore","","Singapore - Premium"
               "Germany - 6","Germany - Super","Germany - Premium",

               ]