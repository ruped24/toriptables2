#!/usr/bin/env python3

import subprocess
import os
import sys
import atexit
import argparse
import json
import urllib.request
import urllib.error
import time

class TorIptables(object):

    def __init__(self):
        self.local_dnsport = "53"
        self.virtual_net = "10.0.0.0/10"
        self.local_loopback = "127.0.0.1"
        self.non_tor_net = ["192.168.0.0/16", "172.16.0.0/12"]
        self.non_tor = ["127.0.0.0/9", "127.128.0.0/10", "127.0.0.0/8"]
        self.tor_uid = subprocess.getoutput("id -ur debian-tor")
        self.trans_port = "9040"
        self.tor_config_file = '/etc/tor/torrc'
        self.torrc = '''
## Inserted by {} for tor iptables rules set
## Transparently route all traffic thru tor on port {}
VirtualAddrNetwork {}
AutomapHostsOnResolve 1
TransPort {}
DNSPort {}
'''.format(os.path.basename(__file__), self.trans_port, self.virtual_net,
           self.trans_port, self.local_dnsport)

    def flush_iptables_rules(self):
        subprocess.call(["iptables", "-F"])
        subprocess.call(["iptables", "-t", "nat", "-F"])

    def load_iptables_rules(self):
        self.flush_iptables_rules()
        self.non_tor.extend(self.non_tor_net)

        @atexit.register
        def restart_tor():
            with open(os.devnull, 'w') as fnull:
                try:
                    tor_restart = subprocess.check_call(
                        ["service", "tor", "restart"],
                        stdout=fnull, stderr=fnull)

                    if tor_restart == 0:
                        print(" [+] Anonymizer status [ON]")
                        self.get_ip()
                except subprocess.CalledProcessError as err:
                    print("[!] Command failed: {}".format(' '.join(err.cmd)))

        subprocess.call(["iptables", "-I", "OUTPUT", "!", "-o", "lo", "!", "-d",
                         self.local_loopback, "!", "-s", self.local_loopback, "-p", "tcp",
                         "-m", "tcp", "--tcp-flags", "ACK,FIN", "ACK,FIN", "-j", "DROP"])
        subprocess.call(["iptables", "-I", "OUTPUT", "!", "-o", "lo", "!", "-d",
                         self.local_loopback, "!", "-s", self.local_loopback, "-p", "tcp",
                         "-m", "tcp", "--tcp-flags", "ACK,RST", "ACK,RST", "-j", "DROP"])
        subprocess.call(["iptables", "-t", "nat", "-A", "OUTPUT", "-m", "owner", "--uid-owner",
                         "%s" % self.tor_uid, "-j", "RETURN"])
        subprocess.call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "udp", "--dport",
                         self.local_dnsport, "-j", "REDIRECT", "--to-ports", self.local_dnsport])

        for net in self.non_tor:
            subprocess.call(["iptables", "-t", "nat", "-A", "OUTPUT", "-d", "%s" % net, "-j",
                             "RETURN"])

        subprocess.call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "--syn", "-j",
                         "REDIRECT", "--to-ports", "%s" % self.trans_port])
        subprocess.call(["iptables", "-A", "OUTPUT", "-m", "state", "--state",
                         "ESTABLISHED,RELATED", "-j", "ACCEPT"])

        for net in self.non_tor:
            subprocess.call(["iptables", "-A", "OUTPUT", "-d", "%s" % net, "-j", "ACCEPT"])

        subprocess.call(["iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "%s" %
                         self.tor_uid, "-j", "ACCEPT"])
        subprocess.call(["iptables", "-A", "OUTPUT", "-j", "REJECT"])

    def get_ip(self):
        print(" [*] Getting public IP, please wait...")
        retries = 0
        my_public_ip = None
        while retries < 12 and not my_public_ip:
            retries += 1
            try:
                with urllib.request.urlopen('https://check.torproject.org/api/ip') as response:
                    my_public_ip = json.loads(response.read().decode())['IP']
            except urllib.error.URLError:
                time.sleep(5)
                print(" [?] Still waiting for IP address...")
            except ValueError:
                break
        if not my_public_ip:
            my_public_ip = subprocess.getoutput('wget -qO - ident.me')
        if not my_public_ip:
            sys.exit(" [!] Can't get public ip address!")
        print(" [+] Your IP is {}".format(my_public_ip))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tor Iptables script for loading and unloading iptables rules')
    parser.add_argument('-l', '--load', action='store_true', help='This option will load tor iptables rules')
    parser.add_argument('-f', '--flush', action='store_true', help='This option flushes the iptables rules to default')
    parser.add_argument('-r', '--refresh', action='store_true', help='This option will change the circuit and gives new IP')
    parser.add_argument('-i', '--ip', action='store_true', help='This option will output the current public IP address')
    args = parser.parse_args()

    try:
        load_tables = TorIptables()
        if os.path.isfile(load_tables.tor_config_file):
            with open(load_tables.tor_config_file) as torrconf_file:
                if 'VirtualAddrNetwork' not in torrconf_file.read():
                    with open(load_tables.tor_config_file, 'a+') as torrconf:
                        torrconf.write(load_tables.torrc)

        if args.load:
            load_tables.load_iptables_rules()
        elif args.flush:
            load_tables.flush_iptables_rules()
            print(" [!] Anonymizer status [OFF]")
        elif args.ip:
            load_tables.get_ip()
        elif args.refresh:
            subprocess.call(['kill', '-HUP', '{}'.format(subprocess.getoutput('pidof tor'))])
            load_tables.get_ip()
        else:
            parser.print_help()
    except Exception as e:
        print("[!] Run as super user: {}".format(e))
