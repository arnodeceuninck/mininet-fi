# Part of this code is taken from the SDN coursera course by Prof. Nick Feamster


from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

# Please add the classes and methods you consider necessary


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']


class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Activating Firewal")

    def _handle_ConnectionUp(self, event):
        # Please add your code here

        # firewall-policies.csv contains an id, mac_0 and mac_1
        # When a connection between a switch and the controller is established (which is the case in this function),
        # the application must install the necessary rules to disable the communication between each MAC pair in the
        # file

        # Convert the policy file to a list of dicts (with the column names in the first row as key)
        with open(policyFile, 'r') as f:
            policy = [dict(zip(['id', 'mac_0', 'mac_1'], line.strip().split(','))) for line in f.readlines()[1:]]

        # Disable communication between each MAC pair
        for rule in policy:
            mac_0 = EthAddr(rule['mac_0'])
            mac_1 = EthAddr(rule['mac_1'])

            def disable_mac_pair(mac_src, mac_dst):
                nf = of.ofp_flow_mod()
                nf.match.dl_src = mac_src  # Ethernet source address
                nf.match.dl_dst = mac_dst  # Ethernet destination address
                nf.actions.append(of.ofp_action_output(port=of.OFPP_NONE))  # Output to no where
                nf.priority = 100
                event.connection.send(nf)

            disable_mac_pair(mac_0, mac_1)
            disable_mac_pair(mac_1, mac_0)

        log.debug("Installed rules in %s", dpidToStr(event.dpid))


def launch():
    core.registerNew(Firewall)
