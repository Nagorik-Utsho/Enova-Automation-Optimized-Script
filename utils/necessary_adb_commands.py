from .necessary_packages import *

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

def is_internet_reachable(driver):
        print("Checking the internet reachability")
        """
        Returns True if ping succeeds, False if it fails.
        """
        try:
            # Run adb shell ping command
            result = subprocess.run(
                ['adb', 'shell', 'ping', '-c', '1', '-W', '10', '8.8.8.8'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output = result.stdout.lower()

            # Check if ping failed (no reply)
            if "64 bytes from" in output:
                print("Internet is reachable")
                return {"status": "FAILED", "message": "Kill switch is not functional"}
            else:
                print("internet is not reachable")
                return {"status": "Passed", "message": "Kill switch is functional"}  # Internet blocked
        except Exception as e:
            print("Error running adb ping:", e)
            return False

