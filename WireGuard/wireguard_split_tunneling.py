from utils.driver_setup import  *
from utils.necessary_generic_utils import server_list, scroll_and_click_in_scrollview
from utils.server_status import in_app_ip
from utils.thrid_party_apps import *
from utils.vpn_activity import *


def wireguard_protocol_split_tunneling_test_executing(driver,server):
    report = {
        "server1": {"name": server}
    }

    server_list(driver)

    scroll_and_click_in_scrollview(driver,server)

    #1.Connet with the server
    connect_server(driver)


    #2.Collect the ip from the application
    ip_info=in_app_ip(driver)
    vpn_ip=ip_info["data"]["ip_address"]


    #3.Get ip from the Chrome
    chrome_ip=get_nord_ip(driver)
    print(chrome_ip)


    if vpn_ip != chrome_ip :
        print("Split tunneling is functional ")
        return {"status": "Passed", "message": "Split tunneling for the functional", "report": report}
    else :
        print("Split tunneling is failed")
        return {"status": "FAILED", "message": "Split tunneling is not fuctional", "report": report}








def split_tunneling_test():

