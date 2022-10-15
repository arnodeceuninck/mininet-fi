from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, OVSBridge
from mininet.nodelib import LinuxBridge


class CustomTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        try:
            # Please insert your code here
            # We recommend to use the method self.addSwitch('s%s'%i, cls=OVSBridge, stp=True)
            # cls and stp parameters allows Mininet to use switchs that build a Spanning Tree

            n = opts['n'] if 'n' in opts else 4

            # Create a mesh network with n switches, all connected to each other and each switch connected to 1 host

            for i in range(n):
                self.addSwitch('s%s' % i, cls=OVSBridge, stp=True)
                self.addHost('h%s' % i)
                self.addLink('s%s' % i, 'h%s' % i)
                for j in range(i):
                    self.addLink('s%s' % i, 's%s' % j)

        except Exception as e:
            raise e  # Used raise instead of return, since return is not allowed in an init method
            # return e


def runNet():
    # topo = CustomTopo()
    # return topo

    topo = CustomTopo(n=6)
    net = Mininet(topo)
    net.start()
    net.pingAll()
    net.stop()


topos = {'custom': (lambda n: CustomTopo(n=n))}

if __name__ == '__main__':
    setLogLevel('info')
    runNet()
