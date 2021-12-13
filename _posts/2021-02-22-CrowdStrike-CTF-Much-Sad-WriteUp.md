---
layout: page
title: "CrowdStrike CTF - Much Sad"
date: 2021-02-22 21:00:00 -0600
tags: ctf osint
intro: Earlier this year, CrowdStrike hosted a CTF centered around three advanced persistent threats. The focus was mainly reverse engineering and binary analysis but there was an OSINT challenge in the `CATAPULT SPIDER` APT group that piqued my interest called "Much Sad".
---
## Intro

Earlier this year, CrowdStrike hosted a CTF centered around three advanced persistent threats. The focus was mainly reverse engineering and binary analysis but there was an OSINT challenge in the `CATAPULT SPIDER` APT group that piqued my interest called "Much Sad".

## Challenge - Much Sad

![](/images/crowdstrike2020/catapultspider.jpg)
Rabid fans of the memetacular Doge and the associated crypto currency, `CATAPULT SPIDER` are trying to turn their obsession into a profit. Watch out for your cat pictures, lest `CATAPULT SPIDER` intrude your networks and extort them for Dogecoin.

We have received some information that `CATAPULT SPIDER` has encrypted a client's cat pictures and successfully extorted them for a ransom of 1337 Dogecoin. The client has provided the ransom note, is there any way for you to gather more information about the adversary's online presence?

## Solution

Opening the file showed me some ASCII art and email address.

```
$ cat much_sad.txt
+------------------------------------------------------------------------------+
|                                                                              |
|                        ,oc,                                                  |
|   BAD CAT.            ,OOxoo,                                  .cl::         |
|                       ,OOxood,                               .lxxdod,        |
|       VERY CRYPTO!    :OOxoooo.                             'ddddoc:c.       |
|                       :kkxooool.                          .cdddddc:::o.      |
|                       :kkdoooool;'                      ;dxdddoooc:::l;      |
|                       dkdooodddddddl:;,''...         .,odcldoc:::::ccc;      |
|                      .kxdxkkkkkxxdddddddxxdddddoolccldol:lol:::::::colc      |
|                     'dkkkkkkkkkddddoddddxkkkkkxdddooolc:coo::;'',::llld      |
|                 .:dkkkkOOOOOkkxddoooodddxkxkkkxddddoc:::oddl:,.';:looo:      |
|             ':okkkkkkkOO0000Okdooodddddxxxxdxxxxdddddoc:loc;...,codool       |
|           'dkOOOOOOkkkO00000Oxdooddxxkkkkkkxxdddxxxdxxxooc,..';:oddlo.       |
|          ,kOOO0OOkOOOOOO00OOxdooddxOOOOOkkkxxdddxxxxkxxkxolc;cloolclod.      |
|         .kOOOO0Okd:;,cokOOkxdddddxOO0OOOOOkxddddddxkxkkkkkxxdoooollloxk'     |
|         l00KKKK0xl,,.',xkkkkkxxxxkOOOkkOkkkkkxddddddxkkkkkkkkxoool::ldkO'    |
|        '00KXXKK0oo''..ckkkkkkkOkkkkkkxl;'.':oddddddxkkkkkkkkkkkdol::codkO.   |
|        xKKXXK00Oxl;:lxkkkkkkOOkkddoc,'lx:'   ;lddxkkkkkkkxkkkkkxdolclodkO.   |
|       ;KKXXXK0kOOOOOkkkkOOOOOOkkdoc'.'o,.  ..,oxkkkOOOkkkkkkkkkkddoooodxk    |
|       kKXKKKKKOOO00OOO00000OOOkkxddo:;;;'';:okOO0O0000OOOOOOOOOkkxddddddx    |
|      .KKKKKKKKOkxxdxkkkOOO000OkkkxkkkkkxxkkkkkOO0KKKKK0OOOO000OOOkkdddddk.   |
|      xKKKKKKc,''''''';lx00K000OOkkkOOOkkkkkkkkO0KKKKKK0OO0000O000Okkxdkkx    |
|     'KK0KKXx. ..    ...'xKKKK00OOOOO000000000OO0KKKKKKKKKKKKK0OOOOOkxdkko    |
|     xKKKKKXx,...      .,dKXKK00000000KKKKKKKKKKKKKKKKKKKK000OOOOOOkxddxd.    |
|    ,KKKKKXKd'.....  ..,ck00OOOOOOkO0KKKKKKKKKKKKKKKKKK0OOOOkkkkkkkxdddo.     |
|    .KKKKK0xc;,......',cok0O0OOOkkkk0KKKK00000KKK000OOOkkkkkkkkkkkxdddd.      |
|    .KKKKK0dc;,,'''''',:oodxkkkkkkkkkOOOOkOOOOkkkkkkkkkkkkkkkOOkkxdddd,       |
|     0KKKKK0x;'.   ...';lodxxkkkkkkddkkkkkkkkkkkkkkkkkkOOOOOkkOkkkxddc        |
|     xKKKKKK0l;'........';cdolc:;;;:lkkkkkkkkkkkkkkkkOO000OOOOOOkxddd.        |
|     :KKKKK00Oxo:,'',''''...,,,;;:ldxkkkkkkkkkkkkkOkkOOOOOOOOkkkxddd'         |
|      oKKKKK0OOkxlloloooolloooodddxkkkkkkkkkkkkkkkkkkkkkkkOOkkkxddd.          |
|       :KKK00OO0OOkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkO0Okkkkkkkkxddd:            |
|        o0KK00000000OOkkkkkkkkkkkkkkkkkkkkkkkkkkO0000Okkkkkkxdo;.             |
|         'd00000000OOOOOOkkkkkkkkkkkkkkkkkOkOO00Okkkkkkkkkkko,                |
|           .oO00000OOOOOkkkkkkkkkkkkkkkkkkOOOOkOOkkkkkkkkko'                  |
|             .;xO0OOOOOOkkkkkkkkkkkkkkkkkkkkkOkkkkkkkkd:.                     |
|                .lxOOOOkkkkkkkkkkkkkkkkkkkxxxkkkkkd:'                         |
|                   .;okkkkkkkkxxkkdxxddxdxdolc;'..                            |
|                       ...',;::::::;;,'...                                    |
|                                                                              |
|                            MUCH SAD?                                         |
|                      1337 DOGE = 1337 DOGE                                   |
|                DKaHBkfEJKef6r3L1SmouZZcxgkDPPgAoE                            |
|              SUCH EMAIL shibegoodboi@protonmail.com                          |
+------------------------------------------------------------------------------+
```

From here, I pulled up the [osintframework.com](osintframework.com) and did some searching for `shibegoodboi@protonmail.com` but no luck.

I then pulled up the OSINT mind map [here](https://medium.com/the-first-digit/osint-how-to-find-information-on-anyone-5029a3c7fd56) created by Petro Cherkasets to keep my searching targeted and logical.

![](/images/crowdstrike2020/email_osint_mindmap.png)

In [Namechk](https://namechk.com/), the username `shibegoodboi` had a hit on [Twitter](https://twitter.com/shibegoodboi).

![](/images/crowdstrike2020/twitter.png)

Going to GitHub, there were several repositories but the one most interesting was the github pages repository - specifically the index.html file.

![](/images/crowdstrike2020/github.png)

```html
<html>
  <head>
    <title>1 DOGE = 1 DOGE</title>
  </head>
  <body>
    <p>1 DOGE = 1 DOGE</p>
    <p>D7sUiD5j5SzeSdsAe2DQYWQgkyMUfNpV2v</p>
    <p>CS{shibe_good_boi_doge_to_the_moon}</p>
    <img src="https://shibefan.github.io/Taka_Shiba.jpg">
  </body>
</html>
```

As we can see, the answer is `CS{shibe_good_boi_doge_to_the_moon}`
