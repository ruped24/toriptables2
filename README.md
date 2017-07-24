# toriptables2

Tor Iptables script is an anonymizer that sets up iptables and tor to route all services and traffic including DNS through the Tor network.

#### Dependencies:
tor

#### [Usage](https://drive.google.com/open?id=0B79r4wTVj-CZVy10Ujg5Vjl5WFk):
```python
toriptables2.py -h
```
#### To test:
* [What is my IP address](http://whatismyipaddress.com)
* [Check Tor Project](https://check.torproject.org)
* [Witch proxy checker](http://witch.valdikss.org.ru)
* [IP leak test](http://www.doileak.com/)
* [DNS leak test](http://dnsleaktest.com)
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
* [BackBox Linux](https://drive.google.com/open?id=0B79r4wTVj-CZQ1ZBeG0xdHFiN0k)

* [Parrot Security OS](http://bit.ly/2b6IjNP)

* [Kali Linux, Rolling Edition](http://bit.ly/1otCXOn)

* [Tor IPTables rules loaded](http://bit.ly/1NjmDLn)

---
## [toriptables2g for GUI Desktop with notification](https://bitbucket.org/ruped24/toriptables2g/src)
#### Dependencies:
tor python-notify

#### [Screenshot](http://bit.ly/2bJO9WA)

---
* [Troubleshooting and FAQ](https://github.com/ruped24/toriptables2/wiki/Troubleshooting)

* [TorIptables2 Install Video](https://www.youtube.com/watch?v=3mEpnzY5ZZo)

* [Optional Installation Methods](https://github.com/ruped24/toriptables2/wiki/Optional-Installation-methods-for-toriptables2.py)

