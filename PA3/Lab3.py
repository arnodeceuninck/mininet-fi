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


class CustomSlice(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)

        # Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
        self.adjacency = defaultdict(lambda: defaultdict(lambda: None))

        '''
        We suggest an structure that relates origin-destination MAC address and port:
        (dpid, origin MAC, destination MAC, port : following dpid)
        The structure of self.portmap is a four-tuple key and a string value.
        The type is:
        (dpid string, src MAC addr, dst MAC addr, port (int)) -> dpid of next switch
        '''

        self.portmap = {
            # ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),
            #  EthAddr('00:00:00:00:00:05'), 200): '00-00-00-00-00-04',
            #
            # """ Please add your logic here """
        }

        udp_config = {
            "port": 200,
            "dst_mac": EthAddr('00:00:00:00:00:05'),
            "host_switch_routes":
                {
                    1: [1, 4, 7],
                    2: [2, 1, 4, 7]
                },
            "hosts_disallowed": [3, 4]
        }

        http_config = {
            "port": 80,
            "dst_mac": EthAddr('00:00:00:00:00:06'),
            "host_switch_routes":
                {
                    2: [2, 5, 7],
                    3: [3, 6, 7],
                    4: [3, 6, 7]
                },
            "hosts_disallowed": [1]
        }

        self.configs = [udp_config, http_config]

        # Add the routes from the configs to the portmap
        for config in self.configs:

            def mac_int_to_mac(mac_int):
                assert 10 > mac_int >= 0  # Else not supported
                return EthAddr("00:00:00:00:00:0" + str(mac_int))

            def dpid_int_to_dpid(dpid_int):
                assert 10 > dpid_int >= 0
                return "00-00-00-00-00-0" + str(dpid_int)

            def get_portmap_key(dpid_int, src_mac_int, dst_mac, port):
                dpid = dpid_int_to_dpid(dpid_int)
                src_mac = mac_int_to_mac(src_mac_int)
                return (dpid, src_mac, dst_mac, port)

            for host, route in config["host_switch_routes"].items():
                for i in range(len(route) - 1):
                    key = get_portmap_key(route[i], host, config["dst_mac"], config["port"])
                    self.portmap[key] = dpid_int_to_dpid(route[i + 1])

    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has connected.", dpid)

    def _handle_LinkEvent(self, event):
        l = event.link
        sw1 = dpid_to_str(l.dpid1)
        sw2 = dpid_to_str(l.dpid2)
        log.debug("link %s[%d] <-> %s[%d]",
                  sw1, l.port1,
                  sw2, l.port2)
        self.adjacency[sw1][sw2] = l.port1
        self.adjacency[sw2][sw1] = l.port2

    def _handle_PacketIn(self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        packet = event.parsed
        tcpp = event.parsed.find('tcp')
        udpp = event.parsed.find('udp')
        '''tcpp=80'''

        # flood, but don't install the rule
        def flood(message=None):
            """ Floods the packet """
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        def install_fwdrule(event, packet, outport):
            msg = of.ofp_flow_mod()
            msg.idle_timeout = 10
            msg.hard_timeout = 30
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.actions.append(of.ofp_action_output(port=outport))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        def forward(message=None):
            this_dpid = dpid_to_str(event.dpid)

            if packet.dst.is_multicast:
                flood()
                return
            else:
                log.debug("Got unicast packet for %s at %s (input port %d):",
                          packet.dst, dpid_to_str(event.dpid), event.port)

                try:
                    """ Add your logic here """"


                except AttributeError:
                    log.debug("packet type has no transport ports, flooding")

                # flood and install the flow table entry for the flood
                install_fwdrule(event, packet, of.OFPP_FLOOD)

        forward()


def launch():
    # Ejecute spanning tree para evitar problemas con topologías con bucles
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    core.registerNew(CustomSlice)
