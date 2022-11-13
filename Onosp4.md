# ONOS-P4
https://github.com/grupogita/ONOSP4-tutorial/wiki
saguti@gmail.com -> Contact if there are problems with e.g. the assignment about ONOS-P4

You have to interact with the onos, mininet, maiben nd p4 images for this tutorial. 

make commands start the image and compile the java application. 

We'll do the [first exercise](https://github.com/grupogita/ONOSP4-tutorial/wiki/Exercise-1:-First-approach-to-the-P4-development-process) during the lecture; the second exercise is our assignment. 

````shell
sudo make start
chmod 755 ./compile.sh # something with chmod, no idea what
sudo make mn-log
sudo make mn-cli


mininet 
h1 ifconfig
h1 ping h2 # doesn't work, since it's not configured yet
````

We have connection, but switch doesn't know how to configure any packets. 

Field sizes must be in bits, not in bytes! (in the RFC it's often in bytes)
