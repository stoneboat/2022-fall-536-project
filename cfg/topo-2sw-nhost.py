"""Custom test topology

Two directly connected switches plus a host for one switch and n-1 host for another:

   host 2,3,...,n --- switch --- switch --- host 1

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class TestTopo( Topo ):
    "A topology looks like host 2,3,...,n --- switch --- switch --- host 1"

    def __init__(self, nHost=2, **opts):
        "Create custom topo with nHost >= 2"

        assert nHost > 1, "host number should be larger than 2"
        Topo.__init__(self, **opts)

        # Add hosts and switches
        rightHost = self.addHost( 'h1' )
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )

        leftHost_list = []
        for i in range(nHost-1):
            leftHost_list.append(self.addHost( 'h'+str(i+2) ))

        # Add links
        for i in range(nHost-1):
            self.addLink( leftHost_list[i], leftSwitch )

        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


topos = { 'testTopo': TestTopo}