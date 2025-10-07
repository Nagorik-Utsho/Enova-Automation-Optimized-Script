from enova_features.connection_disconnection import *
from enova_features.kill_switch import *
from enova_features.server_switch import *
from utils.driver_setup import *
from utils.servers_util import *


def wireguard_protocol_testing(driver):

   #1.Connect & Disconnect check
    #connection_disconnection_execution(driver,'Japan')

   #2. Server switch
    #server_switch_execution(driver, 'Japan', 'Brazil')

   #3.Kill switch check
    kill_switch_execution(driver, 'Japan')









