---
layout: default
title: "Shakti CTF 2021 Help Me Challenge WriteUp"
date: 2021-04-05 13:00:00 -0000
---

# Shakti CTF 2021 Help Me Challenge WriteUp

This was an awesome beginner CTF that has an accompanying conference called [ShaktiCon](https://shakticon.com/). This is an free international conference dedicated to women in cybersecurity.

I focused on the forensic and miscellaneous challenges which were above beginner but not, from my experience, fully intermediate-level. I plan to attend next year and would highly recommend this to others.

## Forensic Challenge: Help Me
>Our department had taken up the responsibility of solving a mysterious case but unfortunately our system crashed. We could only recover this memory dump. Your job is get all the important files from the system and use the files to find out the secret information.  
>Note : The flag consists of 3 parts.

Apart from determining the OS, my first step was to take inventory of the running processes using the `pslist` command. The processes `cmd.exe`, `iexplore.exe`, and `winrar.exe` caught my eye.

```
$ vol.py -f image.vmem --profile=Win7SP1x64 pslist
Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa801ab60630 cmd.exe                1708   1080      1       19      1      0 2021-04-03 05:09:57 UTC+0000                                 
0xfffffa8019a1f970 iexplore.exe           2980    568     17      361      1      0 2021-04-03 05:10:45 UTC+0000                                 
0xfffffa801a729720 iexplore.exe           1092   2980     16      327      1      0 2021-04-03 05:10:46 UTC+0000 
0xfffffa8019cbc760 WinRAR.exe             2836   1080     12      406      1      0 2021-04-03 05:10:38 UTC+0000
```

### Part I

By running `consoles`, I could see the text that appeared in the command prompt window.

```
$ vol.py -f image.vmem --profile=Win7SP1x64 consoles 
**************************************************
ConsoleProcess: conhost.exe Pid: 1144
Console: 0xff716200 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: %SystemRoot%\system32\cmd.exe
Title: C:\Windows\system32\cmd.exe
AttachedProcess: cmd.exe Pid: 1708 Handle: 0x60
----
CommandHistory: 0x26e9c0 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 1 LastAdded: 0 LastDisplayed: 0
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x60
Cmd #0 at 0x2478b0: UGFydCAxlC0gc2hha3RpY3Rme0gwcDM=
----
Screen 0x250f70 X:80 Y:300
Dump:
Microsoft Windows [Version 6.1.7601]                                            
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.                 
                                                                                
C:\Users\alexander>UGFydCAxlC0gc2hha3RpY3Rme0gwcDM=                             
'UGFydCAxlC0gc2hha3RpY3Rme0gwcDM' is not recognized as an internal or external c
ommand,                                                                         
operable program or batch file.                                                 
                                                                                
C:\Users\alexander>     
```

The string in the `consoles` output gave me the first part of the flag:

```
$ echo "UGFydCAxlC0gc2hha3RpY3Rme0gwcDM=" | base64 -d
Part 1 - shaktictf{H0p3
```

### Part II

Since `iexplore.exe` was running, I viewed files opened and websites visited via the `iehistory` tool. A PNG file definitely stood out.

```
$ vol.py -f image.vmem --profile=Win7SP1x64 iehistory
**************************************************
Process: 1080 explorer.exe
Cache type "URL " at 0x27b5200
Record length: 0x100
Location: :2021040320210404: alexander@file:///C:/Users/alexander/Documents/Part%20II.png
Last modified: 2021-04-03 09:52:05 UTC+0000
Last accessed: 2021-04-03 04:22:05 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0x0
**************************************************
```

Using the `dumpfiles` tool, I was able to grab the image.

```
$ vol.py -f image.vmem --profile=Win7SP1x64 dumpfiles -Q 0x000000007e269310 -D ./
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x7e269310   None   \Device\HarddiskVolume1\Users\alexander\Documents\Part II.png
```

![](/images/shaktictf2021/helpme_1.png)

That wasn't exactly a flag so steganography skills were needed. I initially checked it over with GIMP and stegsolve but didn't have any luck. I also ran exiftool and binwalk against it in the hopes the flag would be in either metadata or an embedded file but no luck.

After a lot of head scratching, I came across [zsteg](https://github.com/zed-0xff/zsteg) that can detect hidden data in PNG and BMP files.

```
$ zsteg -a partII.png
[?] 1289 bytes of extra data after image end (IEND), offset = 0x42af7
extradata:0         .. ["\x00" repeated 1289 times]
b1,rgb,lsb,xy       .. text: "Second part : _y0U_l1k3d_"
b1,abgr,msb,xy      .. file: PGP Secret Key -
b2,r,msb,xy         .. text: "}UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
```

### Part III

Pivoting to the `cmdline` tool, I was able to see what the `winrar.exe` process was doing.

```
$ vol.py -f image.vmem --profile=Win7SP1x64 cmdline
************************************************************************
WinRAR.exe pid:   2836
Command line : "C:\Program Files\WinRAR\WinRAR.exe" "C:\Users\alexander\Downloads\L4ST.py.zip"
************************************************************************
```

I used `filescan` to see if the zip file was loaded into memory during the capture.

```
$ vol.py -f image.vmem --profile=Win7SP1x64 filescan
Offset(P)            #Ptr   #Hnd Access Name
------------------ ------ ------ ------ ----
0x000000007ec2c970      2      0 R--r-- \Device\HarddiskVolume1\Users\alexander\Downloads\L4ST.py.zip
```

Dumping the file via `dumpfiles`, I unzipped the archive and found a [python script](/supporting_files/shaktictf2021/L4ST.py).

```
$ vol.py -f image.vmem --profile=Win7SP1x64 dumpfiles -Q 0x000000007ec2c970 -D ./
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x7ec2c970   None   \Device\HarddiskVolume1\Users\alexander\Downloads\L4ST.py.zip
```

Just on a whim, I ran the script and entered a random string "testasdf" before trying to do any reversing.

```
Enter input:  testasdf
yhvydvik
try again:/
``` 

I noticed it appeared to use a simple substitution cipher, so I ran the script again and entered the full alphabet with some special characters.

```
Enter input:  
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()~`,./<>?[]\{}|;':"-=_+
dgfihkjmlonqpsrutwvyx{z}|IJKLMNOPQRSTUVWXYZ[\]^EFGH456789:;<3$E&)(c+/-,e132ACB^`a~>*?'0@b.
try again:/ 
```

A closer look at the script showed I needed to enter a string that, when encoded, would equal `uh27bio:uY<xrA.`.

I was then able to use the conversion list above to find the string `pe/4_dj7pQ9uo<+` that would give me the third portion of the flag.

```
Enter input:  pe/4_dj7pQ9uo<+
uh27bio:uY<xrA.
Yoo.. looks like your flag is complete!!
th15_ch4lL3ng3!}
```

## Final Answer

Putting all the pieces together resulted in the flag `shaktictf{H0p3_y0U_l1k3d_th15_ch4lL3ng3!}`