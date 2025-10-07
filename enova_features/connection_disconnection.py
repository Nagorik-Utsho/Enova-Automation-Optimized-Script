import time
from utils.necessary_generic_utils import server_list, scroll_and_click_in_scrollview
from utils.server_status import server_status_check
from utils.vpn_activity import connect_server, disconnect_server
from utils.report_generator import generate_csv_report

def connection_disconnection_execution_steps(driver, server_name):
    """
    Executes server connection, optimization check, and disconnection steps.
    Logs each step in CSV-ready report.
    """
    report = {
        "server1": {"name": server_name}
    }

    # --------------------------
    # Step 1: Open server list
    try:
        server_list(driver)
        report["server1"]["open_server_list"] = {
            "status": "SUCCESS",
            "message": "Server list opened successfully"
        }
    except Exception as e:
        report["server1"]["open_server_list"] = {
            "status": "FAILED",
            "message": f"Failed to open server list: {e}"
        }

    # --------------------------
    # Step 2: Select server
    try:
        scroll_and_click_in_scrollview(driver, server_name)
        report["server1"]["select_server"] = {
            "status": "SUCCESS",
            "message": f"Server '{server_name}' selected successfully"
        }
    except Exception as e:
        report["server1"]["select_server"] = {
            "status": "FAILED",
            "message": f"Failed to select server '{server_name}': {e}"
        }

    # --------------------------
    # Step 3: Connect with server
    try:
        connect_server(driver)
        time.sleep(0.3)
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
    # Step 4: Check for optimization
    try:
        server_status_check(driver)
        report["server1"]["optimization_check"] = {
            "status": "SUCCESS",
            "message": "Server optimization check passed"
        }
    except Exception as e:
        report["server1"]["optimization_check"] = {
            "status": "FAILED",
            "message": f"Server optimization check failed: {e}"
        }

    # --------------------------
    # Step 5: Disconnect server
    try:
        disconnect_server(driver)
        report["server1"]["disconnect"] = {
            "status": "SUCCESS",
            "message": "Server disconnected successfully"
        }
    except Exception as e:
        report["server1"]["disconnect"] = {
            "status": "FAILED",
            "message": f"Server disconnection failed: {e}"
        }

    # --------------------------
    # Step 6: Generate CSV report
    generate_csv_report(
        report,
        vpn_name="Enova VPN",
        protocol="WireGuard",
        test_name="Connection & Disconnection Test"
    )

    print("✅ Connection/Disconnection test completed and CSV report generated.")



def server_connect_disconnect_execution(driver , server,protocol_name):

    # Run server switch test
    result = connection_disconnection_execution_steps(driver, server,protocol_name)

    # Ensure test passed
    assert result["status"] == "SUCCESS", f"Connection  &  Disconnection failed: {result}"

    # Print results for logs
    print("✅ Connection & Disconnection  test completed successfully")
    print(result["report"])

    # Generate CSV report using the returned report
    generate_csv_report(
        result["report"],
        vpn_name="Enova",
        protocol=protocol_name,
        test_name="Connection & Disconnection"
    )

    print("✅ Server Switch CSV report generated.")

