from utils.necessary_adb_commands import *
from utils.necessary_generic_utils import *
from utils.report_generator import *
from utils.server_status import *
from utils.thrid_party_apps import *
from utils.vpn_activity import *


def server_switch_execution_steps(driver, server1, server2):
    """Check VPN server switching functionality and return a clean report"""

    report = {
        "server1": {"name": server1},
        "server2": {"name": server2}
    }

    print("Checking the server switching functionality for the WireGuard Protocol")

    # 1. Open the server list
    res = server_list(driver)
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to open server list", "details": res}

    # 2. Select countries
    countries = ["Netherlands", "Germany"]
    for country in countries:
        if not scroll_and_click_in_scrollview(driver, country):
            return {"status": "FAILED", "message": f"Country '{country}' not found"}

    # 3. Select 1st server
    if not scroll_and_click_in_scrollview(driver, server1):
        return {"status": "FAILED", "message": f"Target server '{server1}' not found"}

    # 4. Connect server
    res = connect_server(driver)
    report["server1"]["connect"] = res

    # 5. Validate IP
    ip_res = validate_ip(driver)
    report["server1"]["ip_validation"] = ip_res

    # 6. Watch YouTube video (optional step)
    yt_res = watch_youtube(driver)
    report["server1"]["youtube_test"] = yt_res

    # 7. Open server list again
    res = server_list(driver)
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to open server list for server2", "details": res}

    # 8. Select countries again
    for country in countries:
        if not scroll_and_click_in_scrollview(driver, country):
            return {"status": "FAILED", "message": f"Country '{country}' not found for server2"}

    # 9. Select 2nd server
    if not scroll_and_click_in_scrollview(driver, server2):
        return {"status": "FAILED", "message": f"Target server '{server2}' not found"}

    # 10. Switch server
    switch_res = server_switch(driver)
    report["server2"]["switch"] = switch_res

    # 11. Validate IP
    ip_res2 = validate_ip(driver)
    report["server2"]["ip_validation"] = ip_res2

    #12. Reopen Enova
    open_enova(driver)

    # 13. Disconnect
    disconnect_res = disconnect_server(driver)
    report["server2"]["disconnect"] = disconnect_res

    # 14.close the disconnection popup
    res_popup=close_disconnection_report_popup(driver)
    report["server2"]["popup_close"] = res_popup

    return {"status": "SUCCESS", "report": report}

def server_switch_execution(driver, server1, server2):
    """
    Executes server switch test and writes the results to CSV.
    """
    # Run server switch test
    result = server_switch_execution_steps(driver, server1, server2)

    # Ensure test passed
    assert result["status"] == "SUCCESS", f"Server switch failed: {result}"

    # Print results for logs
    print("✅ Server switch test completed successfully")
    print(result["report"])

    # Generate CSV report using the returned report
    generate_csv_report(
        result["report"],
        vpn_name="Enova VPN",
        protocol="WireGuard",
        test_name="Server Switch Test"
    )

    print("✅ Server Switch CSV report generated.")
