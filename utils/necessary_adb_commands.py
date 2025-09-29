from .necessary_packages import time

def open_enova(driver):
    """ Connect to VPN server and run optimization """
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(3)

def reopen_enova(driver):
    # 4 Reopen Enova VPN
    driver.execute_script("mobile: shell",
                          {"command": "monkey -p com.enovavpn.mobile -c android.intent.category.LAUNCHER 1"})
    print("Reopened Enova VPN")
    time.sleep(5)
