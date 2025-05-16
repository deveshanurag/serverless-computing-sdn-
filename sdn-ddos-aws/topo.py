from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class CustomTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1') 

        # Add 6 hosts
        for i in range(1, 7):
            host = self.addHost(f'h{i}', ip=f'10.0.0.{i}')
            self.addLink(host, switch, cls=TCLink, bw=10)  # 10 Mbps link

if __name__ == '__main__':
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=RemoteController, link=TCLink)
    net.start()
    print("🚀 Network is ready. You can use CLI to run tests.")
    CLI(net)
    net.stop()
