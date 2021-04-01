---
layout: default
title: "UMass CTF 2021 WriteUp"
date: 2021-03-31 13:00:00 -0000
---

# UMass CTF 2021 WriteUp

## Notes challenge
> The breach seems to have originated from this host. Can you find the user's mistake? Here is a memory image of their workstation from that day.  
> http://static.ctf.umasscybersec.org/forensics/13096721-bb26-4b79-956f-3f0cddebd49b/image.mem

First things first, I needed to see what processes were running at the time of the memory dump. Based on the name of the challenge, the `notepad` process stood out.

```
$ vol.py -f image.mem --profile=Win7SP1x64 pslist
Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa8000dd0060 notepad.exe            2696   2288      4      309      1      0 2021-03-20 17:59:34 UTC+0000            
```

I suspected the flag was most likely written in the notepad session so I dumped that process.

```
$ vol.py -f image.mem --profile=Win7SP1x64 memdump -p 2696 -D ./
Volatility Foundation Volatility Framework 2.6.1
************************************************************************
Writing notepad.exe [  2696] to 2696.dmp
```

Thanks to Andrea Fortuna's [blog post](https://www.andreafortuna.org/2018/03/02/volatility-tips-extract-text-typed-in-a-notepad-window-from-a-windows-memory-dump/), it was easy to search for the text in the process dump.

```
$ strings -e l ./2696.dmp | grep "umass" -i
UMASS{$3CUR3_$70Rag3}
```

## Scan Me challenge
> The top layer is a lie.  
> http://static.ctf.umasscybersec.org/misc/8e0111c9-d8d0-4518-973d-dbdcbd9d5a42/scan_me.xcf

I wasn't familiar with this extension but [Wikipedia](https://en.wikipedia.org/wiki/XCF_(file_format)) came the rescue and explained this was a way for GIMP to store changes to a single file.

When opened in GIMP, though, I only got a blank white page.

![](/images/umassctf2021/scanme_1.png)

But the clue said the top layer was a lie. I was able to remove the white layer and reveal a broken QR code below.

![](/images/umassctf2021/scanme_2.png)

After reading up on QR codes from this [blog post](https://datagenetics.com/blog/november12013/index.html), I learned they were created to be extremely forgiving so I may not need to reconstruct everything just the `important parts`. Specifically, the `anchors` that tell the software where each corner of the QR code exists.

![](/images/umassctf2021/scanme_3.png)

By simply copy/pasting one of the existing corners into the lower left gave me the link!
https://imgur.com/a/57VgQ8M

![](/images/umassctf2021/scanme_4.png)
