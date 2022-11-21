### a. Collaborator list and Acknowledgement

The markdown file is power by the online md editior [https://stackedit.io](https://stackedit.io/app#) 

The readme content is supported by the 535 course website [https://gitlab.com/purdue-cs536/fall-2022/public](https://gitlab.com/purdue-cs536/fall-2022/public)

### b. Start the ONOS and Mininet dockers

We have provided a `Makefile` containing the commands needed to run Mininet, ONOS, and other configurations. Open four separate command shells and `cd` into the `assignment0` folder.

* In the first shell, **start ONOS**:

```sh
$ cd 2022-fall-536-project
$ make controller
```

This will start the ONOS controller. You will see a lot of information printed on the terminal; wait until it stops -- and it will stop!

* In the second terminal, **start Mininet**:

```sh
$ cd 2022-fall-536-project
$ make mininet nhost=6
```

Once started, you will see the `mininet>` prompt. This indicates that your virtual network is ready and running, and you can now issue commands through this prompt.

This will give us a topology looks like host 2,3,...,n --- switch 1 --- switch 2 --- host 1, you can change the parameter nhost to choose the number clients in one side of the switch. 

Let's try listing the hosts and switches in this network and their connectivity. Enter ...

```sh
mininet> net
```

Output:
```
mininet> net
h1 h1-eth0:s2-eth2

h2 h2-eth0:s1-eth1

h3 h3-eth0:s1-eth2

h4 h4-eth0:s1-eth3

h5 h5-eth0:s1-eth4

h6 h6-eth0:s1-eth5

s1 lo:  s1-eth1:h2-eth0 s1-eth2:h3-eth0 s1-eth3:h4-eth0 s1-eth4:h5-eth0 s1-eth5:h6-eth0 s1-eth6:s2-eth1

s2 lo:  s2-eth1:s1-eth6 s2-eth2:h1-eth0
```

This shows three nodes in this network: `h1`, `h2`, and `s1`. For `h1` and `h2`, their `eth0` interface is connected to switch `s1` `eth1` and `eth2` interfaces, respecitvely.

> **Note:** Visit [http://mininet.org/walkthrough/](http://mininet.org/walkthrough/) to learn more about Mininet and the various commands you can run inside it.

If you try pinging the two hosts (`h1` and `h2`) in Mininet, you will see that the pings won't follow through. From the second terminal, for Mininet, run ...

```sh
mininet> h1 ping -c 4 h2
```

It's because the switch `s1`, at the moment, doesn't know how to route the incoming packets. For that, we will have to connect switch `s1` to the ONOS controller and run a network application (`fwd`) in ONOS that will instruct the switch where to route these packets.

* In the third terminal, **start ONOS CLI**:

To activate the network application `fwd`, start the ONOS command-line interface (CLI) from the third terminal.

```sh
$ cd 2022-fall-536-project
$ make cli 
```

It will prompt a password, which is `rocks` ... and ONOS clearly ROCKS!

Once started, you will see the `onos@root >` prompt. To activate `fwd`, run ...

```sh
onos@root > app activate fwd
```

Output:
``` sh
onos@root > app activate fwd
Activated org.onosproject.fwd
```

> **Note:** Visit [https://wiki.onosproject.org/display/ONOS/The+ONOS+CLI](https://wiki.onosproject.org/display/ONOS/The+ONOS+CLI) to learn various commands that ONOS CLI currently supports. You will find them handy when working on your assignments.

* In the fourth terminal, **run ONOS netcfg** script:

Now, let the ONOS controller know of switch `s1` by passing it the `public/assignments/assignment0/cfg/netcfg.json` file using the `onos-netcfg` script. The JSON file tells the controller through which ip:port to connect to `s1`.

From the fourth terminal, run ...

```sh
$ cd 2022-fall-536-project
$ make netcfg
```

You will see some updates printed on the first terminal, where ONOS is running. Ignore `ERROR`; it's a bug (or typo) in ONOS.

- And then in the same terminal, install Mininet prerequisites and dependencies. (Make sure Mininet is running in another terminal before executing this command).
```sh
$ cd 2022-fall-536-project
$ make mininet-prereqs
```