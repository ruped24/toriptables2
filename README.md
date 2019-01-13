# toriptables2 
![](https://img.shields.io/badge/toriptables2-python_2.7-blue.svg)![](https://img.shields.io/badge/dependencies-tor-orange.svg)

Tor Iptables script is an anonymizer that sets up iptables and tor to route all services and traffic including DNS through the Tor network.

#### Dependencies:
```bash
apt install tor
```

#### [Usage](https://drive.google.com/open?id=0B79r4wTVj-CZVy10Ujg5Vjl5WFk):
```python
toriptables2.py
```
#### To test:
* [Check My IP](http://www.check-my-ip.net)
* [Check Tor Project](https://check.torproject.org)
* [Witch proxy checker](http://witch.valdikss.org.ru)
* [Do I leak](http://www.doileak.com/)
* [DNS leak test](http://dnsleaktest.com)
* [Test IPv6](http://ipv6-test.com/)
* [What every Browser knows about you](http://webkay.robinlinus.com/)


#### To manually change IP w/o reload:
##### Refresh Check Tor Project webpage
```bash
sudo kill -HUP $(pidof tor)
```
#### To automate changing Tor IP:
* [Screenshot](https://drive.google.com/open?id=0B79r4wTVj-CZOGJadlBtWWxPWFk)

* [tor_ip_switcher](https://github.com/ruped24/tor_ip_switcher#tor_ip_switcher)

#### Screenshots:
* [KaliBang Linux Rolling](https://drive.google.com/open?id=1fHtOvukq0j3dcSKk6Yw_d2L3JuXnjNav)

* [Kali Linux, Rolling Edition](https://drive.google.com/open?id=0B79r4wTVj-CZMzlnRWZTcVcyUnc)

* [Tor IPTables rules loaded](https://drive.google.com/open?id=0B79r4wTVj-CZT0NMV2VZRTM1REE)

---
## [toriptables2g for GUI Desktop with notification](https://bitbucket.org/ruped24/toriptables2g/src)
#### Dependencies:
tor python-notify

[Screenshot](https://drive.google.com/open?id=0B79r4wTVj-CZSEdkaTBNOVc5aUU)

---
[Installation Methods](https://github.com/ruped24/toriptables2/wiki/Optional-Installation-methods-for-toriptables2.py)

[Troubleshooting and FAQ](https://github.com/ruped24/toriptables2/wiki/Troubleshooting)
