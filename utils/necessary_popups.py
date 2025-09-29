from .necessary_packages import WebDriverWait, EC, By, time ,  re

def close_disconnection_report_popup(driver):
    wait = WebDriverWait(driver, 120)
    close_popup_xpath = '//android.widget.ImageView[1]'
    try:
        close_popup = wait.until(EC.presence_of_element_located((By.XPATH, close_popup_xpath)))
        close_popup.click()
        time.sleep(2)
        print("✅ Pop-up closed successfully.")
        return {"status": "SUCCESS", "message": "Pop-up closed successfully"}
    except Exception as e:
        print(f"⚠️ Failed to close pop-up: {e}")
        return {"status": "FAILED", "message": f"Failed to close pop-up: {e}"}


def fetch_information(driver, server_name):
    wait = WebDriverWait(driver, 5)
    labels = ["Server Name", "IP Name", "Connection Duration", "Upload Time", "Download Time"]

    info = {}
    try:
        print(f"Disconnection pop up is present for {server_name}")
        all_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//android.view.View[@content-desc]')))
        relevant_elements = all_elements[2:]

        for i, label in enumerate(labels):
            value = relevant_elements[i].get_attribute("content-desc") if i < len(relevant_elements) else "None"
            info[label] = value
            print(f"{label}: {value}")

        return {"status": "SUCCESS", "info": info}
    except Exception:
        print(f"Disconnection pop up is not present for {server_name}")
        for label in labels:
            info[label] = "None"
            print(f"{label}: None")
        return {"status": "FAILED", "info": info}


def successful_server_switch_message(driver):
    wait = WebDriverWait(driver, 5)
    try:
        close_popup = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.ImageView[1]'
        )))
        close_popup.click()
        print("✅ Server switch popup closed successfully.")
        return {"status": "SUCCESS", "message": "Server switch popup closed successfully"}
    except Exception as e:
        print(f"⚠️ Failed to close server switch popup: {e}")
        return {"status": "FAILED", "message": f"Failed to close server switch popup: {e}"}
