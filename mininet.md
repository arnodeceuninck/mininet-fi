# Mininet
## Getting started
````shell
ssh -X mininet@192.168.12.1 # Use ifconfig to determine the ip

sudo mn # the command to start mininet
# Will create the simplest network
````
This will bring you in the mininet interface
````shell
mininet> help 
miniet> help <command> # e.g. help py

mininet> h1 ifconfig # executes the linux command ifconfig on container h1

mininet> net # Gives an overview of the network and how the hosts are connected to the switches

mininet> nodes # Gives an overview of the nodes in the network

mininet> pingall # Pings all hosts in the network
mininet> h1 ping h2 # Pings host h2 from host h1

mininet> xterm h1 # Open a linux console on host h1
# e.g. h1 ping h2 won't work there
#  you must use ping 10.0.0.x instead (you can lookup the ip's using ifconfig)

mininet> exit # Exit mininet
````

You can look at all commands in the [minimet walkthrough](http://mininet.org/walkthrough/)

It's possible to start wireshark from a mininet host. On the mininet host, run sudo wireshark, select the loopback interface, you should see OFP (open flow packets)cptures).

````shell
sudo mn -c # Clear the network, starat a new session
````
## Different topology
````shell
sudo mn --topo single,3 # Create a network with 3 hosts
sudo mn --topo linear,3 # Create a network with 3 hosts connected, to each their own switch, switches in line
sudo mn --topo tree,depth=2,fanout=3 # Create a network tree, two levels, every switch with 3 children
````

## API
The core idea of mininet is to use the PI. All information from the api can be found [here](http://mininet.org/api/annotated.html)

Some of th exaample are on the supplied VM from the lecturs, do an ls in the home directory.

Some important methods from the mininet api:
- Topo is the base clss for miniets
- addSwitch
- AddHost
- addLink
- Mininet
- ... (see slides)

We'll work with the high level view of the slides
````python
from mininet.net import Mininet
from ninnet.topo import LinearTopo

linear = LinearTopo(k=3) # Create a linear topology with 3 hosts
net = Mininet(topo=linear) # Create a new network

net.sart()
net.addHost('h1') # Add a host to the network
net.addSwitch('s1') # Add a switch to the network
net.addLink('h1', 's1') # Add a link between host h1 and switch s1
net.start() # Start the network
net.pingAll() # Ping all hosts in the network
net.stop() # Stop the network
````

## Custom topology
````python
from mininet.topo import Topo # Always import this if you want to create a custom topology


c0= net.addController('c0')
````

### Custom single topology
````python
from mininet.topo import Topo

class SingleSwitchTopo(Topo):
    def build(self, count=1):
        hosts = [self.addHosts('h%d' % (i+1) for i in range(count)) for i in range(count)]
        switch = self.addSwitch('s1')
        for h in hosts:
            self.addLink(h, switch)

topos = {'my_topo': SingleSwitchTopo}

# To run this topology, use the following command
# sudo mn --custom <path to this file> --topo my_topo,3
````

# You can drag and drop files on the server using sftp
````shell
sftp://<server_ip>/
````

Fat  tree assingment is not a real assignmetn

Programming assingment for next week is inth googl classroom.
You need to use a spanning tre for the ssignment. 
Skeleton code is already provided. Don't forget to use a spanning tree to prevent broadcast storms.

## Next slides
-sudo mn --topo single,3 --mac --switch ovsk --controller remote
-- mac is to use mac addresses instead of ip addresses
-- switch ovsk is to use open vswitch kernel module (default)
-- controller remote is to use the remote controller, so you have to do it manually

Ping will fail, because you don't have a controller telling the switches their flow taables.

````shell
mininet> dump-flows # Dump the flows of the switches
````

````shell
dpctl dump-flows tcp:127.0.0.1:6634 # Dump the flows of the switch on port 6634
````
Will be just empty. Let's add an entry

````shell
dpctl add-flow tcp:127.0.0.1:6634 in_ports=1, actions=output:2
dpctl dump-flows tcp:127.0.0.1:6634
````
