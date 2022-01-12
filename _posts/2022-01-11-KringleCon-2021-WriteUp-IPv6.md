---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - IPv6"
date: 2022-01-11 21:00:00 -0600
tags: ctf kringlecon-2021 network
intro: You know IPv4 - now what about IPv6?
---

## Side Quest: IPv6 Investigation

![Goal](/images/kringlecon2021/ipv6_1.png)

The methodology used for IPv4 will be the same for IPv6 - we just need to figure out the right tools.

Step 1: Enumerate hosts that are "up"

Normally, I would just run `nmap` across the subnet as a ping sweep across the subnet. However, with IPv6, the subnets are gigantic are scannin all available IP space is not realistic. So I checked the other available tools and noticed you can use `ping6` to interrogate the `all nodes multicast` address to see live IPs on a subnet. An awesome in-depth explanation of IPv6 scanning can be found [here](https://www.dionach.com/en-us/blog/scanning-ipv6-networks/).

![ping6](/images/kringlecon2021/ipv6_2.png)

Step 2: Scan "up" hosts for open ports

Now that I got a list of live hosts, I then was able to use `nmap` to scan for open ports.

![nmap - host #1](/images/kringlecon2021/ipv6_3.png)

![nmap - host #2](/images/kringlecon2021/ipv6_4.png)

![nmap - host #3](/images/kringlecon2021/ipv6_5.png)

![nmap - host #4](/images/kringlecon2021/ipv5_6.png)

Step 3: Access available hosts via the open ports and profit

Since we have `curl` available to use, I focused on host #4 first and investigated port 80.

![curl](/images/kringlecon2021/ipv6_7.png)

From there, I was able to run `netcat` against port 9000 and find the flag:

![netcat](/images/kringlecon2021/ipv6_8.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
* [Scanning IPv6 Networks](https://www.dionach.com/en-us/blog/scanning-ipv6-networks/)
* [Using curl with IPv6](https://stackoverflow.com/questions/41843247/how-to-curl-using-ipv6-address/52036287)