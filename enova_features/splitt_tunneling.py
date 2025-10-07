from utils.necessary_generic_utils import *
from utils.server_status import *
from utils.thrid_party_apps import *
from utils.vpn_activity import *


def split_tunneling_test_executing(driver, server):
    """
    Executes WireGuard Split Tunneling test and generates a CSV report with step-wise validation.
    """
    report = {
        "server1": {"name": server}
    }

    # --------------------------
    # Step 1: Open server list
    try:
        server_list(driver)
        scroll_and_click_in_scrollview(driver, server)
        report["server1"]["open_server_list"] = {
            "status": "SUCCESS",
            "message": "Server list opened and server selected successfully"
        }
    except Exception as e:
        report["server1"]["open_server_list"] = {
            "status": "FAILED",
            "message": f"Failed to open/select server: {e}"
        }

    # --------------------------
    # Step 2: Connect to server
    try:
        connect_server(driver)
        report["server1"]["connect"] = {
            "status": "SUCCESS",
            "message": "Server connected successfully"
        }
    except Exception as e:
        report["server1"]["connect"] = {
            "status": "FAILED",
            "message": f"Server connection failed: {e}"
        }

    # --------------------------
    # Step 3: IP validation for split tunneling
    try:
        ip_info = in_app_ip(driver)
        vpn_ip = ip_info["data"]["ip_address"]
        chrome_ip = get_nord_ip(driver)
        if vpn_ip != chrome_ip:
            status = "SUCCESS"
            message = "Split tunneling functional: VPN IP differs from Chrome IP"
        else:
            status = "FAILED"
            message = "Split tunneling failed: VPN IP matches Chrome IP"

        report["server1"]["ip_validation"] = {
            "status": status,
            "message": message
        }

    except Exception as e:
        report["server1"]["ip_validation"] = {
            "status": "FAILED",
            "message": f"IP validation failed: {e}"
        }