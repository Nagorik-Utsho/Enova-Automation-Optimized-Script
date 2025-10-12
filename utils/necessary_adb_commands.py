from .necessary_packages import *

def open_enova(driver):
    """Reopen Enova VPN main activity"""
    print("Reopening the VPN application ")
    try:
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        time.sleep(3)
        return {"status": "SUCCESS", "message": "Application successfully reopened"}
    except Exception as e:
        return {"status": "FAILED", "message": f"Failed to reopen app: {e}"}




def reopen_enova(driver):
    try :
        # 4 Reopen Enova VPN
        driver.execute_script("mobile: shell",
                              {"command": "monkey -p com.enovavpn.mobile -c android.intent.category.LAUNCHER 1"})
        print("Reopened Enova VPN")
        time.sleep(5)
        return {"status": "Passed", "message": "Application successfully reopened"}
    except Exception as e :
        return {"status": "FAILED", "message": f"Failed to reopen app: {e}"}

def force_stop_enova(driver):
    try:
        # Run adb command to force-stop the app
        subprocess.run(
            ['adb', 'shell', 'am', 'force-stop', 'com.enovavpn.mobile'],
            check=True
        )
        print("Enova VPN app has been force-stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to force-stop Enova VPN: {e}")



def go_home(driver):
    """
    Return to Home screen safely (no force-stop of launcher).
    """
    try:
        if driver:
            driver.execute_script("mobile: shell", {"command": "input keyevent 3"})
        else:
            import subprocess
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '3'], check=True)
        print("Returned to Home screen (launcher).")
        return {"status": "SUCCESS", "message": "Returned to Home screen"}
    except Exception as e:
        print(f"Failed to return home: {e}")
        return {"status": "FAILED", "message": f"Failed to return home: {e}"}



def is_internet_reachable(driver):
    """
    Checks if the internet is reachable to validate Kill Switch functionality.
    Returns a dictionary with 'status' and 'message'.
    """
    print("Checking the internet reachability for Kill Switch...")
    try:
        # Run adb ping command
        result = subprocess.run(
            ['adb', 'shell', 'ping', '-c', '1', '-W', '10', '8.8.8.8'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stdout.lower()

        # If ping succeeds, internet is reachable → Kill switch FAILED
        if "64 bytes from" in output:
            print("Internet is reachable → Kill Switch FAILED")
            return {"status": "FAILED", "message": "Kill switch is not functional: internet reachable"}

        # If ping fails, internet is blocked → Kill switch SUCCESS
        print("Internet is not reachable → Kill Switch SUCCESS")
        return {"status": "SUCCESS", "message": "Kill switch is functional: internet blocked"}

    except Exception as e:
        # Any exception is treated as failure
        print(f"Error running adb ping: {e}")
        return {"status": "FAILED", "message": f"Kill switch test failed: {e}"}






def tapping_vpn_settings(device_id):
    # Reference values from original device
    REFERENCE_Y = 2402
    REFERENCE_SMALL_Y = 195
    TAP_X = 111

    # Get device screen size via adb
    result = subprocess.run(
        ["adb", "-s", device_id, "shell", "wm", "size"],
        capture_output=True, text=True
    )
    output = result.stdout.strip()
    print(f"adb wm size output: '{output}'")  # Debug print

    if "Physical size:" not in output:
        print(f"Failed to get device size. Output: '{output}'")
        return

    try:
        _, size_str = output.split(": ")
        device_width, device_height = map(int, size_str.split("x"))
    except Exception as e:
        print(f"Error parsing screen size: {e}")
        return

    # Calculate proportional small Y
    small_y2 = int((device_height * REFERENCE_SMALL_Y) / REFERENCE_Y)

    # Tap using adb command
    subprocess.run(
        ["adb", "-s", device_id, "shell", "input", "tap", str(TAP_X), str(small_y2)]
    )

    print(f"Tapped at ({TAP_X}, {small_y2}) on device with height {device_height}")



