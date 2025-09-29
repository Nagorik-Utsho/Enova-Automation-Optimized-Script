
from utils.necessary_generic_utils import scroll_and_click_in_scrollview
from utils.report_generator import generate_csv_report
from utils.vpn_activity import *
from utils.necessary_adb_commands import *
from utils.server_status import  *
from utils.thrid_party_apps import *
from utils.necessary_popups import *
import random



def check_wireguard_protocol_servers_status(driver,server):

    #1.Open the server list
    serverlist(driver)

    #2.Open the Drop_downs
    print(" Countries name ")
    countries = ["Netherlands", "Germany"]
    for country in countries:
            print(f"🔍 Looking for {country}...")
            if not scroll_and_click_in_scrollview(driver, country):
                print(f"❌ Country '{country}' not found in list.")
                return

    #3.Select server
    print(f"🔎 Searching for target server: {server}...")
    if not scroll_and_click_in_scrollview(driver, server):
        print(f"❌ Target server '{server}' not found, skipping connection.")
        return

    #4.Click to connect the server
    connect_server(driver)
    #5.Check for the server optimization
    server_status_check(driver)
    #5.IP validation
    validate_ip(driver)
    #6.Reopen enova vpn
    open_enova(driver)
    #6.Disconnect server
    disconnect_server(driver)
    #7.close the disconnection popup
    close_disconnection_report_popup(driver)





def check_wireguard_protocol_server_switch(driver, server1, server2):
    """Check VPN server switching functionality and return a clean report"""

    report = {
        "server1": {"name": server1},
        "server2": {"name": server2}
    }

    print("Checking the server switching functionality for the WireGuard Protocol")

    # 1. Open the server list
    res = serverlist(driver)
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
    res = serverlist(driver)
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


def wireguard_servers(driver):
  # Selecting the server name
    #servers=["India - 3"]
    servers = [ "India - 3", "Netherlands - 1",
                "Netherlands - 3", "Brazil",
                    "Singapore - 1", "Germany - 1", "Germany - 6",
                   "Germany Warrior", "Canada", "Poland"]

    # for server in servers :
    #       check_wireguard_protocol_servers_status(driver,server)


    result = check_wireguard_protocol_server_switch(driver, 'India - 3', 'Netherlands - 3')

    assert result["status"] == "SUCCESS", f"Server switch failed: {result}"
    print("Server switch test completed successfully")
    print(result["report"])
    generate_csv_report(result["report"],"","WireGuard")














