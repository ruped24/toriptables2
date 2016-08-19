# toriptables2
Tor Iptables script is an anonymizer that sets up iptables and tor to route all services and traffic including DNS through the tor network.

#####Dependencies:
tor

#####Usage:
```python
toriptables2.py -h
```
#####To test:
* http://ipchicken.com
* https://check.torproject.org
* http://witch.valdikss.org.ru
* https://ipleak.net
* http://dnsleaktest.com


#####To change IP w/o reload:
```bash
sudo kill -HUP $(pidof tor)
```
###### Screenshots:
* http://bit.ly/1otCXOn
* http://bit.ly/1NjmDLn

##[toriptables2g for GUI Desktop with notification](https://bitbucket.org/ruped24/toriptables2g/src)
#####Dependencies:
tor python-notify

###### Screenshot:
* http://bit.ly/2bJO9WA
