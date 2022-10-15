'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")

    """This event will be raised each time a switch will connect to the controller"""

    def _handle_ConnectionUp(self, event):

        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this 
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)

        """ Add your logic here """

        # There are 4 switches.
        # S1 is connected to s2 and s4
        # S2 is connected to s1 and s3
        # S3 is connected to s2 and s4
        # S4 is connected to s1 and s3

        # H1 and h2 are connected to s1
        # H3 and h4 are connected to s3

        # We want to create two slices.
        # Slice 1: 10Mbps bandwidht with path h2-s1-s4-s3-h4
        # Slice 2: 100Mbps bandwidht with path h1-s1-s2-s3-h3

        def add_redirect_port_rule(in_port, out_port):
            msg = of.ofp_flow_mod()
            msg.match.in_port = in_port
            msg.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(msg)

        def connect_ports_both_ways(port1, port2):
            add_redirect_port_rule(port1, port2)
            add_redirect_port_rule(port2, port1)

        if dpid == '00-00-00-00-00-01':
            # We're in switch 1
            connect_ports_both_ways(2, 4)  # Slice 1
            connect_ports_both_ways(1, 3)  # Slice 2
        if dpid == '00-00-00-00-00-02':
            # We're in switch 2
            connect_ports_both_ways(1, 2)  # Slice 2
        if dpid == '00-00-00-00-00-03':
            # We're in switch 3
            connect_ports_both_ways(2, 4)  # Slice 1
            connect_ports_both_ways(1, 3)  # Slice 2
        if dpid == '00-00-00-00-00-04':
            # We're in switch 4
            connect_ports_both_ways(1, 2)  # Slice 1

        log.debug("Slice rules installed on %s", dpid)


def launch():
    log.debug("Launching Topology Slice")
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
