---
layout: default
title: "MemLabs Lab 4 WriteUp"
date: 2021-02-04 21:00:00 -0600
---
# MemLabs Lab 4 WriteUp

## Intro
This write up will cover the fourth memory challenge published on GitHub and managed by [stuxnet9999](https://github.com/stuxnet999/MemLabs/tree/master/Lab%204).

## Challenge - Obsession
Challenge Description
My system was recently compromised. The Hacker stole a lot of information but he also deleted a very important file of mine. I have no idea on how to recover it. The only evidence we have, at this point of time is this memory dump. Please help me.

Note: This challenge is composed of only 1 flag.

The flag format for this lab is: inctf{s0me_l33t_Str1ng}

## Solution
Using `iehistory`, I wanted to check what files were recently opened on the device. Below are the most interesting entries I found.

```
Process: 1944 explorer.exe
Cache type "URL " at 0x4515500
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Downloads/galf.jpeg
Last modified: 2019-06-25 12:42:58 UTC+0000
Last accessed: 2019-06-25 12:42:58 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa4
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517700
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/secrets.txt
Last modified: 2019-06-25 14:34:28 UTC+0000
Last accessed: 2019-06-25 14:34:28 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa4
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517800
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/flag.txt.txt
Last modified: 2019-06-25 12:47:15 UTC+0000
Last accessed: 2019-06-25 12:47:15 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa8
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517900
Record length: 0x100
Location: Visited: eminem@file:///C:/Program%20Files/Reference%20Assemblies/Microsoft/Framework/v3.0/RedistList/Important.txt.txt
Last modified: 2019-06-25 15:08:33 UTC+0000
Last accessed: 2019-06-25 15:08:33 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xe0
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517a00
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/New%20Text%20Document.txt
Last modified: 2019-06-26 15:27:07 UTC+0000
Last accessed: 2019-06-26 15:27:07 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xb4
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517b00
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/Important.txt.txt
Last modified: 2019-06-25 15:06:00 UTC+0000
Last accessed: 2019-06-25 15:06:00 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xac
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517c00
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/Screenshot1.png
Last modified: 2019-06-27 13:26:38 UTC+0000
Last accessed: 2019-06-27 13:26:38 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa8
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517d00
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/Important.txt
Last modified: 2019-06-26 12:01:46 UTC+0000
Last accessed: 2019-06-26 12:01:46 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa8
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4517e00
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/Screenshot1.png
Last modified: 2019-06-29 07:29:06 UTC+0000
Last accessed: 2019-06-29 07:29:06 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa8
**************************************************
Process: 1944 explorer.exe
Cache type "URL " at 0x4518000
Record length: 0x100
Location: Visited: eminem@file:///C:/Users/eminem/Desktop/Flag%20not%20here.bmp
Last modified: 2019-06-29 07:29:04 UTC+0000
Last accessed: 2019-06-29 07:29:04 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xb0
**************************************************
Process: 3012 explorer.exe
Cache type "URL " at 0x20f5000
Record length: 0x100
Location: Visited: SlimShady@file:///C:/Users/SlimShady/Desktop/Important.txt
Last modified: 2019-06-29 07:29:43 UTC+0000
Last accessed: 2019-06-29 07:29:43 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xac
```

I then went to use `filescan` to determine if this data was in the memory dump.

```
$ cat filescan | grep "galf"
0x000000003e8ad250     14      0 R--r-- \Device\HarddiskVolume2\Users\eminem\Desktop\galf.jpeg
0x000000003e8d1c80      2      0 RW-rw- \Device\HarddiskVolume2\Users\eminem\AppData\Roaming\Microsoft\Windows\Recent\galf.lnk

$ vol.py -f memdump.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003e8ad250 -D ~/Downloads/Lab4
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x3e8ad250   None   \Device\HarddiskVolume2\Users\eminem\Desktop\galf.jpeg

$ cat filescan | grep "Important"
0x000000003f939720      2      0 RW-rw- \Device\HarddiskVolume2\Users\SlimShady\AppData\Roaming\Microsoft\Windows\Recent\Important.lnk
0x000000003fc398d0     16      0 R--rw- \Device\HarddiskVolume2\Users\SlimShady\Desktop\Important.txt

$ vol.py -f memdump.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003fc398d0 -D ~/Downloads/Lab4
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x3fc398d0   None   \Device\HarddiskVolume2\Users\SlimShady\Desktop\Important.txt

$ cat filescan | grep "Screenshot"
0x000000003e8d19e0     16      0 R--r-- \Device\HarddiskVolume2\Users\eminem\Desktop\Screenshot1.png
0x000000003e8e5ba0      2      0 RW-rw- \Device\HarddiskVolume2\Users\eminem\AppData\Roaming\Microsoft\Windows\Recent\Screenshot1.lnk

$ vol.py -f memdump.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003e8d19e0 -D ~/Downloads/Lab4
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x3e8d19e0   None   \Device\HarddiskVolume2\Users\eminem\Desktop\Screenshot1.png
```

Unfortunately, I was only able to grab two image files but they were red herrings and held no clues. The file dump of `Important.txt` didn't work so I assumed that was the target I needed to recover.

I notice Volatility had an `mftparser` module and then I had a lightbulb moment! If a file is under a certain size, its contents are stored in the MFT! As a side note, these special files are known as resident files in the MFT.

Using a combination of `grep`, `head`, and `tail`, I was able to pull out the data of interest from the `mftparser` output.

```
$ vol.py -f memdump.raw --profile=Win7SP0x64 mftparser > mftparser
Volatility Foundation Volatility Framework 2.6.1

$ cat mftparser | grep "Important" -n
132198:2019-06-26 12:02:23 UTC+0000 2019-06-29 07:29:43 UTC+0000   2019-06-29 07:29:43 UTC+0000   2019-06-29 07:29:43 UTC+0000   Users\SLIMSH~1\AppData\Roaming\MICROS~1\Windows\Recent\Important.lnk
164457:2019-06-27 13:14:13 UTC+0000 2019-06-27 13:14:13 UTC+0000   2019-06-27 13:14:13 UTC+0000   2019-06-27 13:14:13 UTC+0000   Users\SlimShady\Desktop\Important.txt

$ head -164480 mftparser | tail -50
Object ID: 40000000-0000-0000-00c0-020000000000
Birth Volume ID: 00c00200-0000-0000-00c0-020000000000
Birth Object ID: 312c63a3-0000-ffff-ffff-ffff82794711
Birth Domain ID: 00000000-0000-0000-0000-000000000000

***************************************************************************
***************************************************************************
MFT entry found at offset 0x3bd8ac00
Attribute: In Use & File
Record Number: 60583
Link count: 2


$STANDARD_INFORMATION
Creation                       Modified                       MFT Altered                    Access Date                    Type
------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
2019-06-27 13:14:13 UTC+0000 2019-06-27 13:26:12 UTC+0000   2019-06-27 13:26:12 UTC+0000   2019-06-27 13:14:13 UTC+0000   Archive

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2019-06-27 13:14:13 UTC+0000 2019-06-27 13:14:13 UTC+0000   2019-06-27 13:14:13 UTC+0000   2019-06-27 13:14:13 UTC+0000   Users\SlimShady\Desktop\IMPORT~1.TXT

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2019-06-27 13:14:13 UTC+0000 2019-06-27 13:14:13 UTC+0000   2019-06-27 13:14:13 UTC+0000   2019-06-27 13:14:13 UTC+0000   Users\SlimShady\Desktop\Important.txt

$OBJECT_ID
Object ID: 7726a550-d498-e911-9cc1-0800275e72bc
Birth Volume ID: 80000000-b800-0000-0000-180000000100
Birth Object ID: 99000000-1800-0000-690d-0a0d0a0d0a6e
Birth Domain ID: 0d0a0d0a-0d0a-6374-0d0a-0d0a0d0a0d0a

$DATA
0000000000: 69 0d 0a 0d 0a 0d 0a 6e 0d 0a 0d 0a 0d 0a 63 74   i......n......ct
0000000010: 0d 0a 0d 0a 0d 0a 0d 0a 66 7b 31 0d 0a 0d 0a 0d   ........f{1.....
0000000020: 0a 5f 69 73 0d 0a 0d 0a 0d 0a 5f 6e 30 74 0d 0a   ._is......_n0t..
0000000030: 0d 0a 0d 0a 0d 0a 5f 45 51 75 34 6c 0d 0a 0d 0a   ......_EQu4l....
0000000040: 0d 0a 0d 0a 5f 37 6f 5f 32 5f 62 55 74 0d 0a 0d   ...._7o_2_bUt...
0000000050: 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 5f 74 68 31 73   ..........._th1s
0000000060: 5f 64 30 73 33 6e 74 0d 0a 0d 0a 0d 0a 0d 0a 5f   _d0s3nt........_
0000000070: 6d 34 6b 65 0d 0a 0d 0a 0d 0a 5f 73 33 6e 0d 0a   m4ke......_s3n..
0000000080: 0d 0a 0d 0a 0d 0a 73 33 7d 0d 0a 0d 0a 47 6f 6f   ......s3}....Goo
0000000090: 64 20 77 6f 72 6b 20 3a 50                        d.work.:P

***************************************************************************
***************************************************************************
MFT entry found at offset 0x3bddf000
Attribute: In Use & File
```

As we can see, the flag is `inctf{1_is_n0t_EQu4l_7o_2_bUt_th1s_d0s3nt_m4ke_s3ns3}`

## References
[MFT Resident Files](http://ntfs.com/ntfs-files-types.htm#:~:text=When%20a%20file's%20attributes%20can,in%20the%20MFT%20file%20record.)
