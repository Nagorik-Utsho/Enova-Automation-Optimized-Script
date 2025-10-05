from .necessary_packages import *
from .helpers import *


'''Settings Option'''
def vpn_settings_menu(driver):
    """ Go for the VPN Setting option """
    wait=WebDriverWait(driver,30)
    try :
        """Click on the settings icon"""
        wait_and_click(driver,'//android.widget.Button[contains(@content-desc,"Settings")]')
        return {"status": "SUCCESS", "message": "Successfully clicked on the settings menu"}
    except Exception as e:
        print(e)
        return {"status": "Failed ", "message": "Failed to click on the settings menu"}


'''VPN settings'''
def vpn_settings_options(driver):
    wait=WebDriverWait(driver,30)
    try:
        print("CLicking on the vpn settings option ")
        wait_and_click(driver,'//android.widget.ImageView[@content-desc="VPN settings"]')

        return {"status": "SUCCESS", "message": "Successfully clicked on the VPN Settings Option"}
    except Exception as e:
        print(e)
        return {"status": "Failed ", "message": "Failed to click on the VPN settings option"}


''''''