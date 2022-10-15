# PA3
Run the topology
## Part 1
### Running topology
````shell
sudo mn --custom Topo.py --topo p3-1 --controller remote,port6633 --link tc
````
(--link tc is required to get bandwith working in e.g. `self.addLink(h1,s1,bw=10)`)

### Run pox
Should be simultaneously ran in a second window
````shell
sudo ./pox.py log.level --DEBUG pox.misc.topologySlice
````

## Part 2
## Running topology
````shell
sudo mn --custom Topo.py --topo p3-2 --controller remote,port6633 --link tc
````

## Testing
````shell
mininet> h5 iperf -s  -p 200 &
mininet> h6 iperf -s -p 80 &
mininet> h1 iperf -c h5 -p 200 -t 2 -i 1
mininet> h3 iperf -c h6 -p 80 -t 2 -i 1
````