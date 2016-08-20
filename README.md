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
[Kali Linux](http://bit.ly/1otCXOn)

[Parrot Security OS](http://bit.ly/2b6IjNP)

[IP Tables rules loaded](http://bit.ly/1NjmDLn)


##[toriptables2g for GUI Desktop with notification](https://bitbucket.org/ruped24/toriptables2g/src)
#####Dependencies:
tor python-notify

###### Screenshot:
[Tor Iptables2 with desktop notification](http://bit.ly/2bJO9WA)
