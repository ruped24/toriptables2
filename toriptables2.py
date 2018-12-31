#! /usr/bin/env python2
# Written by Rupe version 2
#
"""
Tor Iptables script is an anonymizer
that sets up iptables and tor to route all services
and traffic including DNS through the tor network.
"""

from __future__ import print_function
from commands import getoutput
from subprocess import call, check_call, CalledProcessError
from os.path import isfile, basename
from os import devnull
from sys import stdout, stderr
from atexit import register
from argparse import ArgumentParser
from json import load
from urllib2 import urlopen, URLError
from time import sleep


class TorIptables(object):

  def __init__(self):
    self.local_dnsport = "53"  # DNSPort
    self.virtual_net = "10.0.0.0/10"  # VirtualAddrNetwork
    self.local_loopback = "127.0.0.1" # Local loopback 
    self.non_tor_net = ["192.168.0.0/16", "172.16.0.0/12"]
    self.non_tor = ["127.0.0.0/9", "127.128.0.0/10", "127.0.0.0/8"]
    self.tor_uid = getoutput("id -ur debian-tor")  # Tor user uid
    self.trans_port = "9040"  # Tor port
    self.tor_config_file = '/etc/tor/torrc'
    self.torrc = r'''
## Inserted by %s for tor iptables rules set
## Transparently route all traffic thru tor on port %s
VirtualAddrNetwork %s
AutomapHostsOnResolve 1
TransPort %s
DNSPort %s
''' % (basename(__file__), self.trans_port, self.virtual_net, 
       self.trans_port, self.local_dnsport)

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
        tor_restart = check_call(
            ["service", "tor", "restart"],
              stdout=fnull, stderr=fnull)

        if tor_restart is 0:
          print(" {0}".format(
              "[\033[92m+\033[0m] Anonymizer status \033[92m[ON]\033[0m"))
          print(" {0}".format(
              "[\033[92m*\033[0m] Getting public IP, please wait..."))
          retries = 0
          my_public_ip = None
          while retries < 12 and not my_public_ip:
            retries += 1
            try:
              my_public_ip = load(urlopen('http://ident.me/.json'))['address']
            except URLError:
              sleep(5)
              print(" [\033[93m?\033[0m] Still waiting for IP address...")
          print
          if not my_public_ip:
            my_public_ip = getoutput('wget -qO - v4.ifconfig.co')
          if not my_public_ip:
            exit(" \033[91m[!]\033[0m Can't get public ip address!")
          print(" {0}".format("[\033[92m+\033[0m] Your IP is \033[92m%s\033[0m" % my_public_ip))
      except CalledProcessError as err:
        print("\033[91m[!] Command failed: %s\033[0m" % ' '.join(err.cmd))

    # See https://trac.torproject.org/projects/tor/wiki/doc/TransparentProxy#WARNING
    # See https://lists.torproject.org/pipermail/tor-talk/2014-March/032503.html
    call(["iptables", "-I", "OUTPUT", "!", "-o", "lo", "!", "-d",
          self.local_loopback, "!", "-s", self.local_loopback, "-p", "tcp",
          "-m", "tcp", "--tcp-flags", "ACK,FIN", "ACK,FIN", "-j", "DROP"])
    call(["iptables", "-I", "OUTPUT", "!", "-o", "lo", "!", "-d",
          self.local_loopback, "!", "-s", self.local_loopback, "-p", "tcp",
          "-m", "tcp", "--tcp-flags", "ACK,RST", "ACK,RST", "-j", "DROP"])

    call(["iptables", "-t", "nat", "-A", "OUTPUT", "-m", "owner", "--uid-owner",
          "%s" % self.tor_uid, "-j", "RETURN"])
    call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "udp", "--dport",
          self.local_dnsport, "-j", "REDIRECT", "--to-ports", self.local_dnsport])

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
      print(" {0}".format(
          "[\033[93m!\033[0m] Anonymizer status \033[91m[OFF]\033[0m"))
    else:
      parser.print_help()
  except Exception as err:
    print("[!] Run as super user: %s" % err[1])
