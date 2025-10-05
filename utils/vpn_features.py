from .necessary_generic_utils import retry
from .necessary_packages import WebDriverWait, EC, By, time
from .necessary_popups import close_disconnection_report_popup
from .necessary_adb_commands import *





# Example Appium test
def test_kill_switch(driver):
    """
    Test kill switch functionality
    """
    # Assuming VPN is OFF and kill switch is ON
    internet_status = is_internet_reachable(driver)

    if internet_status:
        print("Kill switch FAILED: Internet is reachable while VPN is disconnected.")
    else:
        print("Kill switch PASSED: Internet is blocked as expected.")













