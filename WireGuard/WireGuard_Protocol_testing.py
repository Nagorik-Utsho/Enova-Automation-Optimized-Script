from enova_features.connection_disconnection import connection_disconnection_execution
from enova_features.kill_switch import kill_switch_execution
from enova_features.server_switch import server_switch_execution
from utils.driver_setup import setup_driver
from utils.servers_util import *


def wireguard_protocol_testing(driver):

   #1.Connect & Disconnect check
    #connection_disconnection_execution(driver,'Japan')

   #2. Server switch
    #server_switch_execution(driver, 'Japan', 'Brazil')

   #3.Kill switch check
    kill_switch_execution(driver, 'Japan')









