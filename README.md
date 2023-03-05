Streams RF statistics from Cisco 9800 guestshell to external system
-------------------------------------------------------------

Collects: "show ap auto-rf dot11 5ghz" output.
Sends:
- AP name
- Slot number
- Radio Type
- Channel utilization
- Client count
- Number of channel changes
- Last channel change

**datastream.py**
CLI command runner and parser, runs on 9800 WLC

Requirements:
- requests
- cli (Cisco : pre-installed)


**textmonitor.py**
Flask app receives and displays statistics in console, tested on Windows 11 & Debian 11

Requirements:
- flask
- tabulate

**webmonitor.py**
Flask app receives and displays statistics in web interface, tested on Windows 11 & Debian 11

Requirements:
- flask

Installation 9800
-----------------
Enable guestshell (9800 WLC supports guestshell only on service port)

```
conf t
iox
app-hosting appid guestshell
 app-vnic management guest-interface 0
guestshell enable
```
Notes:

1. Guestshell requires DNS, add nameserver to /etc/resolv.conf
2. Use yum to install git, nano (optional)
3. Use pip to install requirements
4. Disable logging for CLI library, by setting LOGFILE = None in CLI init
(/usr/lib/python3.6/site-packages/cli/\_\_init\_\_.py)
4. Clone this repository to WLC (https://github.com/Johnny8Bit/guestshell9800)
5. Edit IP address of receiving station in **datastream.py**

Run
---
```
WLC9800#guestshell
[guestshell@guestshell ~]$ cd /home/guestshell/guestshell9800/
[guestshell@guestshell guestshell9800]$ python3 datastream.py
```

```
@debian:~/guestshell9800$ python3 textmonitor.py
```
or
```
@debian:~/guestshell9800$ python3 webmonitor.py
```

Sample output
-------------
```
Last update: 2022-11-13 11:10:05

AP Name             Slot  Radio               Ch.Util %    Clients  Ch.Changes    Last Ch.Change
----------------  ------  ----------------  -----------  ---------  ------------  -------------------
AP-3                   1  802.11ax - 5 GHz            2          1  0             11/13/2022 09:39:15
AP687D.B45C.A734       1  802.11ax - 5 GHz            1          1  0             11/13/2022 09:35:53
AP687D.B45C.A734       2  802.11ax - 5 GHz            0          0  -             -
AP-3                   2  802.11ax - 5 GHz            0          0  -             -
```
