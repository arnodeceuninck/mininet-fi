# PA3
Run the topology
## SSH
I also used this in the previous assignments, but noticed I didn't document my commands anywhere.
My virtualbox network is set to "Bridged adapter"

Get the ipadress of the VM by running this command in the VM:
```bash
ifconfig
````
e.g. in my case (for now, it might change sometimes), I get as eth0 inet adress `192.168.0.143`.
    
Then I can ssh into the VM from my host machine by running this command:
```bash
ssh -X mininet@192.168.0.143
```
-X is important to be able to attach to the display (e.g. when using xterm)

I set up a shared folder from this repo to the VM, so I can edit the files in PyCharm (with GitHub Copilot, which saves me a lot of time). Now get them to the home folder of the VM with these commands (if you've also set up a mounted folder with the same name):
```bash
sudo cp -R /media/sf_mininet-fi/ .
sudo chmod -R 777 sf_mininet-fi
```

Note: putting files on the VM was a lot easier using sftp, e.g. using [WinSCP](https://winscp.net/download/WinSCP-5.21.5-Setup.exe). Here I could just drag the required files to the VM.

## Part 1
### Running topology
Put Topo.py in the folder from which you're running this command (in my case the home folder) and run this:
````shell
sudo mn --custom Topo.py --topo p3-1 --controller remote,port=6633 --link tc
````
(--link tc is required to get bandwith working in e.g. `self.addLink(h1,s1,bw=10)`)

### Run pox
Should be simultaneously ran in a second window
````shell
sudo ./pox.py log.level --DEBUG pox.misc.topologySlice
````

I can't test the bandwith (ping works, but iperf gives connection refused), but let's just assume it works.

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