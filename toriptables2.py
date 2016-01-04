#! /usr/bin/env python
# Written by Rupe version 2
"""
Tor Iptables script is an anonymizer
that sets up iptables and tor to route all services
and traffic including DNS through the tor network.
"""

from __future__ import print_function
from commands import getoutput
from subprocess import call, check_call, CalledProcessError
from os.path import isfile
from os import devnull
from sys import stdout, stderr
from atexit import register
from argparse import ArgumentParser


class TorIptables(object):

  def __init__(self):
    self.local_dnsport = "53"  #  DNSPort
    self.virtual_net = "10.0.0.0/10"  #  VirtualAddrNetwork
    self.non_tor_net = ["192.168.0.0/16", "172.16.0.0/12"]
    self.non_tor = ["127.0.0.0/9", "127.128.0.0/10", "127.0.0.0/8"]
    self.tor_uid = getoutput("id -ur debian-tor")  # Tor user uid
    self.trans_port = "9040"  # Tor port
    self.tor_config_file = '/etc/tor/torrc'
    self.torrc = '''
## Transparently route all traffic thru tor on port %s
VirtualAddrNetwork %s
AutomapHostsOnResolve 1
TransPort %s
DNSPort %s
''' % (self.trans_port, self.virtual_net, self.trans_port, self.local_dnsport)

  def flush_iptables_rules(self):
    call(["iptables", "-F"])
    call(["iptables", "-t", "nat", "-F"])

  def load_iptables_rules(self):
    self.flush_iptables_rules()
    self.non_tor.extend(self.non_tor_net)

    @register
    def restart_tor():
      fnull = open(devnull, 'w')
      try:
        tor_restart = check_call(["service", "tor", "restart"], 
                                  stdout=fnull, stderr=fnull)
        if tor_restart is 0:
          print(" {0}".format("[\033[92m+\033[0m] Anonymizer \033[92mON\033[0m"))
      except CalledProcessError as err:
        print("\n[!] Command failed: %s" % err.cmd)

    call(["iptables", "-t", "nat", "-A", "OUTPUT", "-m", "owner", "--uid-owner",
          "%s" % self.tor_uid, "-j", "RETURN"])
    call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "udp", "--dport", "53",
          "-j", "REDIRECT", "--to-ports", "53"])

    for net in self.non_tor:
      call(["iptables", "-t", "nat", "-A", "OUTPUT", "-d", "%s" % net, "-j",
            "RETURN"])

    call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "--syn", "-j",
          "REDIRECT", "--to-ports", "%s" % self.trans_port])

    call(["iptables", "-A", "OUTPUT", "-m", "state", "--state",
          "ESTABLISHED,RELATED", "-j", "ACCEPT"])

    for net in self.non_tor:
      call(["iptables", "-A", "OUTPUT", "-d", "%s" % net, "-j", "ACCEPT"])

    call(["iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "%s" %
          self.tor_uid, "-j", "ACCEPT"])
    call(["iptables", "-A", "OUTPUT", "-j", "REJECT"])


if __name__ == '__main__':
  parser = ArgumentParser(
      description=
      'Tor Iptables script for loading and unloading iptables rules')
  parser.add_argument('-l',
                      '--load',
                      action='store_true',
                      help='This option will load tor iptables rules')
  parser.add_argument('-f',
                      '--flush',
                      action='store_true',
                      help='This option flushes the iptables rules to default')
  args = parser.parse_args()

  try:
    load_tables = TorIptables()
    if isfile(load_tables.tor_config_file):
      if not 'VirtualAddrNetwork' in open(load_tables.tor_config_file).read():
        with open(load_tables.tor_config_file, 'a+') as torrconf:
          torrconf.write(load_tables.torrc)

    if args.load:
      load_tables.load_iptables_rules()
    elif args.flush:
      load_tables.flush_iptables_rules()
      print(" {0}".format("[\033[93m!\033[0m] Anonymizer \033[91mOFF\033[0m"))
    else:
      parser.print_help()
  except Exception as err:
    print("[!] Run as super user: %s" % err[1])
