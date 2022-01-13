---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - WiFi Dongle & Thermostat"
date: 2022-01-12 21:00:00 -0600
tags: ctf kringlecon-2021 wifi api
intro: An intro to WiFi and API stuff
---

## Objective: Thaw Frost Tower's Entrance

> Turn up the heat to defrost the entrance to Frost Tower. Click on the Items tab in your badge to find a link to the Wifi Dongle's CLI interface. Talk to Greasy Gopherguts outside the tower for tips.

By running `iwconfig`, it showed the current settings for the WiFi dongle (it wasn't connected to anything) and it had one card: `wlan0`.

Once the device was in range, though, with the same network as the thermostat, I could see nearby networks available via `iwlist`.

![Initial commands](/images/kringlecon2021/wifi_dongle_1.png)

To connect the dongle to the network, I simply ran `iwconfig` and specified the dongle's WiFi card and the target ESSID (Extended Service Set Identification).

![Connecting to the network](/images/kringlecon2021/wifi_dongle_2.png)

Then, once on the network, I used curl to interact with the thermostat's API. The base page provided documentation on the available endpoints and syntax.

![Connecting to the API](/images/kringlecon2021/wifi_dongle_3.png)

![API docs](/images/kringlecon2021/wifi_dongle_4.png)

The only endpoint we have access to without credentials is the `api/cooler` which appears to have a `temperature` setting we can adjust.

![API endpoints](/images/kringlecon2021/wifi_dongle_5.png)

Simply setting the temperature to above freezing (above 0 deg. C) got the door unfrozen!

![Changing the temperature](/images/kringlecon2021/wifi_dongle_6.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [iwconfig man page](https://linux.die.net/man/8/iwconfig)
- [iwlist man page](https://linux.die.net/man/8/iwlist)
- [curl man page](https://linux.die.net/man/1/curl)