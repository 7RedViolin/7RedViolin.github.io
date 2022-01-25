---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Customer Complaint Analysis"
date: 2022-01-21 21:00:00 -0500
tags: ctf kringlecon-2021 network wireshark
intro: How to search a PCAP via wireshark
---

## Objective: Customer Complaint Analysis
> A human has accessed the Jack Frost Tower network with a non-compliant host. Which three trolls complained about the human? Enter the troll names in alphabetical order separated by spaces.

We're given a packet capture (pcap) to analyze the web traffic. First things first, I checked out the TCP streams. This feature of Wireshark will organize the packets so you can follow the thread between the two IPs of interest.

![TCP Stream #1](/images/kringlecon2021/pcap_1.png)

From there, I noticed the packets containing the form input all have the same content-type so I filtered the pcap to only include `urlencoded-form`.

![Filtered pcap](/images/kringlecon2021/pcap_2.png)

Now it's just a matter of scrolling through the forms and finding the guest complaint. In this case, the guest Muffy VonDuchess Sebastian is in room 1024.

![Guest complaint](/images/kringlecon2021/pcap_3.png)

From here, we can pivot to find all complaints involving room 1024.

![Troll complaint #1](/images/kringlecon2021/pcap_4.png)

![Troll complaint #2](/images/kringlecon2021/pcap_5.png)

![Troll complaint #3](/images/kringlecon2021/pcap_6.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [Wireshark TCP streams](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html)