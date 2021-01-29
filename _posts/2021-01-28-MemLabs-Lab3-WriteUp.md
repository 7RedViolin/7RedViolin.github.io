---
layout: default
title: "MemLabs Lab 3 WriteUp"
date: 2021-01-28 21:00:00 -0600
---
# MemLabs Lab 3 WriteUp

## Intro
This write up will cover the third memory challenge published on GitHub and managed by [stuxnet9999 (aka Abhiram Kumar)](https://github.com/stuxnet999/MemLabs/tree/master/Lab%203).

## Challenge - The Evil's Den
A malicious script encrypted a very secret piece of information I had on my system. Can you recover the information for me please?

Note-1: This challenge is composed of only 1 flag. The flag split into 2 parts.

Note-2: You'll need the first half of the flag to get the second.

You will need this additional tool to solve the challenge:

`$ sudo apt install steghide`

The flag format for this lab is: inctf{s0me_l33t_Str1ng}

## Solution

I start by running `iehistory` to see if there's any interesting files that were recently opened. I wasn't disappointed and found several leads.

```
Process: 5300 explorer.exe
Cache type "DEST" at 0x64d819
Last modified: 2018-09-30 15:17:32 UTC+0000
Last accessed: 2018-09-30 09:47:34 UTC+0000
URL: hello@file:///C:/Users/hello/Desktop/evilscript.py
****************************************************
Process: 5300 explorer.exe
Cache type "DEST" at 0x35bc1a9
Last modified: 2018-09-30 15:17:50 UTC+0000
Last accessed: 2018-09-30 09:47:52 UTC+0000
URL: hello@file:///C:/Users/hello/Desktop/vip.txt
****************************************************
Process: 5300 explorer.exe
Cache type "URL " at 0x1cc7500
Record length: 0x100
Location: Visited: hello@file:///C:/Users/hello/Desktop/suspision1.jpeg
Last modified: 2018-09-30 09:45:53 UTC+0000
Last accessed: 2018-09-30 09:45:53 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0xa8
****************************************************
Process: 5300 explorer.exe
Cache type "DEST" at 0x61d93a1
Last modified: 2018-09-30 15:15:59 UTC+0000
Last accessed: 2018-09-30 09:46:00 UTC+0000
URL: hello@file:///C:/Users/hello/Desktop/evilscript.py.py
```
To verify these files existed in the memory dump, I used `grep` against the `filescan` output. Then, I used `dumpfiles` to output the info.

```
$ vol.py -f memdump.raw --profile=Win7SP1x86 dumpfiles -Q 0x000000003e727e50 -D ~/Downloads/Lab3/
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x3e727e50   None   \Device\HarddiskVolume2\Users\hello\Desktop\vip.txt

$ vol.py -f memdump.raw --profile=Win7SP1x86 dumpfiles -Q 0x000000003de1b5f0 -D ~/Downloads/Lab3/
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x3de1b5f0   None   \Device\HarddiskVolume2\Users\hello\Desktop\evilscript.py.py

$ vol.py -f memdump.raw --profile=Win7SP1x86 dumpfiles -Q 0x0000000004f34148 -D ~/Downloads/Lab3/
Volatility Foundation Volatility Framework 2.6.1
DataSectionObject 0x04f34148   None   \Device\HarddiskVolume2\Users\hello\Desktop\suspision1.jpeg
```

The vip.txt file appeared to be base64 encoded. However, decoding the string only resulted in gibberish.

```
$ cat vip_txt.dat
am1gd2V4M20wXGs3b2U=

$ cat vip_txt.dat | base64 -d
jm`wex3m0\k7oe
base64: invalid input
```
I then opened the evilscript_py_py.dat file and found the string is both base64 and XOR encoded.

```
$ cat evilscript_py_py.dat
import sys
import string

def xor(s):
	a = ''.join(chr(ord(i)^3) for i in s)
	return a

def encoder(x):
	return x.encode("base64")

if __name__ == "__main__":
	f = open("C:\\Users\\hello\\Desktop\\vip.txt", "w")
	arr = sys.argv[1]
	arr = encoder(xor(arr))
	f.write(arr)
	f.close()
```

To reverse the script . . .

```
$ cat decode_script.py
import sys
import string

arr = "am1gd2V4M20wXGs3b2U="

a = arr.decode("base64")

x = ''.join(chr(ord(i)^3) for i in a)

print(x)
```

That gave me the first half of the flag:

```
$ python decode_script.py
inctf{0n3_h4lf
```

The next item on the to-do list was to analyze the suspision1.jpeg file. The file itself seemed pretty uninteresting.

![](/images/memlabs3/suspision1.jpeg)

Using steghide and the first half of the flag, I was able to extract the hidden file.

```
$ steghide extract -sf suspision1_jpeg.dat
Enter passphrase:
wrote extracted data to "secret text".

$ cat 'secret text'
_1s_n0t_3n0ugh}
```

That makes the complete flag:
`inctf{0n3_h4lf_1s_n0t_3n0ugh}`

## References
[Steghide Examples](https://www.2daygeek.com/easy-way-hide-information-inside-image-and-sound-objects/)  
[Reversing XOR](https://stackoverflow.com/questions/14279866/what-is-inverse-function-to-xor)
