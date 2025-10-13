from WireGuard.WireGuard_Protocol_testing import *
from utils.necessary_adb_commands import *
from utils.necessary_generic_utils import *
from utils.server_status import *
from utils.vpn_activity import *
from utils.driver_setup import *
driver=setup_driver()

countries,servers = wireguard_protocol_servers(driver)

def servers_status_checking_execution_steps(driver,server):
    # Get the countries and servers
    countries= wireguard_protocol_servers(driver)

    #1.Open the server list
    server_list(driver)

    #2.Open the Drop_downs
    print(" Countries name ")

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


def server_status_checking_executing(driver):

    #Checking the servers
     for server in servers :
         servers_status_checking_execution_steps(driver,server)