from .necessary_adb_commands import tapping_vpn_settings
from .necessary_packages import *
from .helpers import *
from  utils.driver_setup import *
device_udid,android_version=get_connected_device_info()
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


'''going back to the Home page'''
def go_back_to_homepage(driver):

   tapping_vpn_settings(device_udid)

   #Go to the home page
   wait_and_click(driver,'//android.widget.Button[contains(@content-desc,"Home")]')

