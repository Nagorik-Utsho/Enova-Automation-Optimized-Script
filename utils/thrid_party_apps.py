from .necessary_packages import time, TimeoutException, WebDriverWait, EC, NoSuchElementException, By

def watch_youtube(driver):
    """Watch a YouTube video while keeping VPN connection alive"""
    try:
        print("Video opening function")
        youtube_video_id = "9iDXWx7GtZQ"

        # 1. Kill only the app UI/foreground activity but leave VPN service running
        driver.execute_script("mobile: shell", {
            "command": "am kill --user 0 com.enovavpn.mobile"
        })
        print("Killed Enova VPN UI (connection remains active in background)")
        time.sleep(2)

        # 2. Open YouTube video (default opens in Brave browser)
        youtube_intent = f"am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v={youtube_video_id}"
        driver.execute_script("mobile: shell", {"command": youtube_intent})
        print("Opened YouTube video (in browser)")
        time.sleep(40)  # Simulate watching

        # 3. Close Brave browser and YouTube
        driver.execute_script("mobile: shell", {"command": "am force-stop com.brave.browser"})
        driver.execute_script("mobile: shell", {"command": "am force-stop com.google.android.youtube"})
        print("Closed Brave browser and YouTube app")
        time.sleep(10)

        # 4. Reopen Enova VPN
        driver.execute_script("mobile: shell",
                              {"command": "monkey -p com.enovavpn.mobile -c android.intent.category.LAUNCHER 1"})
        print("Reopened Enova VPN")
        time.sleep(5)

        return {"status": "SUCCESS", "message": "YouTube video watched and VPN reopened successfully"}

    except Exception as e:
        print(f"❌ Failed in watch_youtube: {e}")
        return {"status": "FAILED", "message": str(e)}


def get_ip_from_app(driver):
    """Fetch public IP from a third-party app"""
    app_package = "cz.webprovider.whatismyipaddress"
    app_activity = "cz.webprovider.whatismyipaddress.MainActivity"

    try:
        print("Getting the IP from the third-party app")
        driver.execute_script("mobile: shell", {"command": f"am start -n {app_package}/{app_activity}"})
        time.sleep(5)

        refresh_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/refresh_info"))
        )
        refresh_button.click()
        time.sleep(5)

        ip_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/zobraz_ip"))
        )
        ip = ip_element.text.strip()
        print("IP from the My IP app:", ip)

        return {"status": "SUCCESS", "ip": ip, "message": "IP fetched successfully"}

    except TimeoutException:
        print("❌ IP fetch timed out.")
        return {"status": "FAILED", "ip": None, "message": "IP fetch timed out"}

    except NoSuchElementException as e:
        print(f"❌ IP element not found: {e}")
        return {"status": "FAILED", "ip": None, "message": str(e)}

    finally:
        driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
        print("📱 Returned to home screen.")
