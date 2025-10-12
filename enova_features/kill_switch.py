from utils.necessary_adb_commands import *
from utils.necessary_generic_utils import *
from utils.report_generator import *
from utils.vpn_activity import *

'''Verify the functionality of the kill switch feature in WireGuard Protocol'''
def kill_switch_execution_steps(driver, server1):
    report = {
        "server1": {"name": server1}
    }

    # 1. Open server list
    res = server_list(driver)
    report["server1"]["open_server_list"] = res
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to open server list", "report": report}
    #
    # # 2. Select countries
    # for country in ["Netherlands", "Germany"]:
    #     step_name = f"select_country_{country}"
    #     success = scroll_and_click_in_scrollview(driver, country)
    #     res = {
    #         "status": "SUCCESS" if success else "FAILED",
    #         "message": f"Country '{country}' selected" if success else f"Country '{country}' not found"
    #     }
    #     report["server1"][step_name] = res
    #     if not success:
    #         return {"status": "FAILED", "message": res["message"], "report": report}

    # 3. Select server
    success = scroll_and_click_in_scrollview(driver, server1)
    res = {
        "status": "SUCCESS" if success else "FAILED",
        "message": f"Server '{server1}' selected" if success else f"Server '{server1}' not found"
    }
    report["server1"]["select_server"] = res
    if not success:
        return {"status": "FAILED", "message": res["message"], "report": report}

    # 4. Connect server
    res = connect_server(driver)
    report["server1"]["connect_server"] = res
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to connect server", "report": report}

    # 5. Turn ON Kill Switch
    res = turn_on_kill_switch(driver)
    report["server1"]["kill_switch_on"] = res
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to turn ON kill switch", "report": report}

    #6. Go back to home page
    go_back_to_homepage(driver)

    # 7. Disconnect server
    res = disconnect_server(driver)
    report["server1"]["disconnect_server"] = res
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to disconnect server", "report": report}

    # 8. Test Kill Switch
    res = is_internet_reachable(driver)
    report["server1"]["kill_switch_test"] = res
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Kill switch is not functional", "report": report}

    # 9. Turn OFF Kill Switch
    res = turn_off_kill_switch(driver)
    report["server1"]["kill_switch_off"] = res
    if res["status"] == "FAILED":
        return {"status": "FAILED", "message": "Failed to turn OFF kill switch", "report": report}

    # 10. Go back to VPN home again
    #6. Go back to home page
    go_back_to_homepage(driver)


    # All steps passed
    return {"status": "SUCCESS", "message": "Kill switch test passed", "report": report}


def kill_switch_execution(driver, server_name):
    # Run kill switch test
    kill_switch_result = kill_switch_execution_steps(driver, server_name)

    # Ensure test passed
    assert kill_switch_result["status"] == "SUCCESS", f"Kill switch test failed: {kill_switch_result}"

    # Generate CSV report using the report returned from the test
    generate_csv_report(
        kill_switch_result["report"],
        vpn_name="Enova VPN",
        protocol="WireGuard",
        test_name="Kill Switch Test"
    )

    print("✅ Kill Switch execution completed and CSV generated.")

