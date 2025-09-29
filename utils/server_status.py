from .vpn_activity import disconnect_server, connect_server
from .necessary_popups import close_disconnection_report_popup, successful_server_switch_message
from .necessary_packages import WebDriverWait, EC, By, time, re, TimeoutException
from .thrid_party_apps import get_ip_from_app
from .necessary_adb_commands import reopen_enova
from .necessary_generic_utils import retry

@retry(max_attempts=3, delay=2)
def server_status_check(driver):
    """Check if server needs optimization and disconnect if needed"""
    try:
        print("Checking for server optimization")
        max_attempts = 2
        attempt = 1

        while attempt <= max_attempts:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
                    ))
                )
                server_name = not_optimized_servers(driver)
                disconnect_server(driver)
                return {"status": "SUCCESS", "server": server_name, "message": "Server optimized and disconnected"}

            except TimeoutException:
                if attempt == max_attempts:
                    return {"status": "PASSED", "message": "No optimization needed"}
                attempt += 1
                time.sleep(2)

    except Exception as e:
        return {"status": "FAILED", "message": f"Server status check failed: {e}"}


@retry(max_attempts=3, delay=2)
def not_optimized_servers(driver):
    """Handle server optimization popup"""
    try:
        wait = WebDriverWait(driver, 10)
        optimization_msg = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'))
        )
        full_text = optimization_msg.get_attribute("content-desc")
        print("Full text:", full_text)
        time.sleep(3)

        match = re.search(r"Unfortunately,\s*(.*?)\s*is not optimized", full_text)
        server_name = match.group(1).strip() if match else None

        if server_name:
            print("Server name:", server_name)
        else:
            print("No server name found")

        successful_server_switch_message(driver)
        return server_name

    except Exception as e:
        print(f"Failed in not_optimized_servers: {e}")
        return None


@retry(max_attempts=3, delay=2)
def in_app_ip(driver):
    """Get connected VPN server and IP"""
    try:
        wait = WebDriverWait(driver, 30)
        server_info = {"Server_name": "", "ip_address": ""}

        get_serverinfo = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//android.view.View[contains(@content-desc,"Connected")]'))
        )

        for elem in get_serverinfo:
            content_desc = elem.get_attribute("content-desc")
            if content_desc:
                lines = content_desc.split("\n")
                if len(lines) >= 7:
                    server_info["Server_name"] = lines[1]
                    server_info["ip_address"] = lines[2]
                    print(f"Server: {lines[1]}, IP: {lines[2]}")
                    break

        if not server_info["Server_name"] or not server_info["ip_address"]:
            return {"status": "FAILED", "message": "No server info found"}

        return {"status": "SUCCESS", "data": server_info}

    except Exception as e:
        print(f"Failed to gather server info: {e}")
        return {"status": "FAILED", "message": str(e)}


@retry(max_attempts=3, delay=2)
def validate_ip(driver):
    """Validate VPN IP against third-party app"""
    try:
        print("Now in IP validation function")
        vpn_info = in_app_ip(driver)
        if vpn_info["status"] != "SUCCESS":
            return {"status": "FAILED", "message": "VPN info not available"}

        server_name = vpn_info["data"]["Server_name"]
        vpn_ip = vpn_info["data"]["ip_address"]

        external_info = get_ip_from_app(driver)
        if external_info["status"] != "SUCCESS":
            return {"status": "FAILED", "message": "External IP not available"}

        external_ip = external_info["ip"]
        if vpn_ip == external_ip:
            print(f"✅ {vpn_ip} == {external_ip}, IP matched")
            return {"status": "SUCCESS", "server": server_name, "message": "IP matched"}
        else:
            print(f"❌ {vpn_ip} != {external_ip}, IP mismatch")
            return {"status": "FAILED", "server": server_name, "message": "IP mismatch"}

    except Exception as e:
        return {"status": "FAILED", "message": str(e)}
