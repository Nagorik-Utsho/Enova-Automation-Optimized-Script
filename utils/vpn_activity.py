from .navigation import *
from .necessary_generic_utils import retry
from .helpers import *
from .necessary_popups import close_disconnection_report_popup






def connect_server(driver):
    """Connect to VPN server"""
    try:
        print("Connect with the  server ")

        wait = WebDriverWait(driver, 60)
        connect_button = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_button.click()
        time.sleep(2)
        return {"status": "SUCCESS", "message": "Server connected successfully"}
    except Exception as e:
        print("Failed to connect with the server")
        return {"status": "FAILED", "message": f"Failed to connect to server: {e}"}

@retry()
def disconnect_server(driver):
    """Disconnect the VPN server"""
    try:
        wait = WebDriverWait(driver, 5)
        turn_on_button = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]'
        )))
        turn_on_button.click()
        disconnect_button = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]'
        )))
        disconnect_button.click()
        time.sleep(3)
        close_disconnection_report_popup(driver)
        return {"status": "SUCCESS", "message": "Server disconnected successfully"}
    except Exception as e:
        return {"status": "FAILED", "message": f"Failed to disconnect: {e}"}


@retry()
def server_switch(driver):
    """Switch the VPN server"""
    try:
        wait = WebDriverWait(driver, 120)
        click_switch = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.view.View[@content-desc="Switch"]'
        )))
        click_switch.click()
        return {"status": "SUCCESS", "message": "Server switched successfully"}
    except Exception as e:
        return {"status": "FAILED", "message": f"Server switch failed: {e}"}



''' Kill switch turn on '''

def turn_on_kill_switch(driver):
    try:
        #Settings menu
        vpn_settings_menu(driver)
        #VPN settings
        vpn_settings_options(driver)

        print("Now in the wait and click block")

        wait_and_click(driver, '//android.view.View[contains(@content-desc,"Internet kill switch")]')
        wait_and_click(driver, '//android.view.View[@content-desc="OPEN SETTINGS"]')
        wait_and_click(driver, '//android.widget.ImageView[@content-desc="Settings"]')
        wait_and_click(driver, '(//android.widget.Switch[@resource-id="android:id/switch_widget"])[1]')
        wait_and_click(driver, '(//android.widget.Switch[@resource-id="android:id/switch_widget"])[2]')
        wait_and_click(driver, '//android.widget.Button[@resource-id="android:id/button1"]')
        return {"status": "SUCCESS", "message": "Kill switch turned on successfully"}
    except Exception as e:
        print(e)
        return {"status": "FAILED", "message": "Failed to turn on the kill switch"}



def turn_off_kill_switch(driver):
    try:
        #Settings menu
        vpn_settings_menu(driver)
        #VPN settings
        vpn_settings_options(driver)
        wait_and_click(driver, '//android.view.View[contains(@content-desc,"Internet kill switch")]')
        wait_and_click(driver, '//android.view.View[@content-desc="OPEN SETTINGS"]')
        wait_and_click(driver, '//android.widget.ImageView[@content-desc="Settings"]')
        wait_and_click(driver, '(//android.widget.Switch[@resource-id="android:id/switch_widget"])[1]')
        return {"status": "SUCCESS", "message": "Kill switch turned off  successfully"}

    except Exception as e:
        print("Failed to turn of the kill switch",{e})
        return {"status": "Failed", "message": "Kill switch turning off  failed"}

