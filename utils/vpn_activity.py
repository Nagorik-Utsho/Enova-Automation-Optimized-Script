from .necessary_generic_utils import retry
from .necessary_packages import WebDriverWait, EC, By, time
from .necessary_popups import close_disconnection_report_popup

def serverlist(driver):
    """Go to the Server list to check all the servers"""
    try:
        wait = WebDriverWait(driver, 60)
        server = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'))
        )
        server.click()
        time.sleep(2)
        return {"status": "SUCCESS", "message": "Server list opened successfully"}
    except Exception as e:
        return {"status": "FAILED", "message": f"Server list not found: {e}"}


def connect_server(driver):
    """Connect to VPN server"""
    try:
        wait = WebDriverWait(driver, 60)
        connect_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_button.click()
        time.sleep(2)
        return {"status": "SUCCESS", "message": "Server connected successfully"}
    except Exception as e:
        return {"status": "FAILED", "message": f"Failed to connect to server: {e}"}


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
