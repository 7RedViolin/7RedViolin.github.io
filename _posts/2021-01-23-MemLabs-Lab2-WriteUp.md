---
layout: page
title: "MemLabs Lab 2 WriteUp"
date: 2021-01-23 21:00:00 -0600
tags: memory ctf forensics
intro: This write up will cover the second memory challenge published on GitHub and managed by stuxnet9999 (aka Abhiram Kumar).
---
## Intro
This write up will cover the second memory challenge published on GitHub and managed by stuxnet9999 (aka Abhiram Kumar). https://github.com/stuxnet999/MemLabs/tree/master/Lab%202

## Challenge - A New World
One of the clients of our company, lost the access to his system due to an unknown error. He is supposedly a very popular "environmental" activist. As a part of the investigation, he told us that his go to applications are browsers, his password managers etc. We hope that you can dig into this memory dump and find his important stuff and give it back to us.

## Flag 1
I always like to start with listing the processes to see what was running or recently exited on the machine at the time of the memory dump.

![](/images/memlabs2/pslist_1.png)

![](/images/memlabs2/pslist_2.png)

![](/images/memlabs2/pslist_3.png)

Items of interest were all the chrome.exe processes and keepass.exe since the "go-to applications" mentioned were internet browsers and password managers.

One thing I didn't want to forget was the line "very popular 'environmental' activist". Could this have been a reference to an environment variable? I checked using the `envars` command.

![](/images/memlabs2/envars.png)

It appeared the `NEW_TMP` variable is base64 encoded. Decoding the string gave me the first flag!

![](/images/memlabs2/base64_decode.png)

## Flag 2

For the second flag, I ran `iehistory` - this showed me not only URLs visited but also files opened.

![](/images/memlabs2/iehistory_1.png)

![](/images/memlabs2/iehistory_2.png)

If these files were loaded into memory at the time of the dump, they would be in the `filescan` output.

![](/images/memlabs2/filescan_1.png)

![](/images/memlabs2/filescan_2.png)

The only ones available were the png and kdbx files. I dumped these using the `dumpfiles` command.

![](/images/memlabs2/dumpfiles_1.png)

Opening up the PNG was a little disappointing . . .

![](/images/memlabs2/password_png.png)

But wait - what was that in the lower right hand corner?

![](/images/memlabs2/password_png_fineprint.png)

Hm . . . What could that password be for? Maybe that KDBX file? From Google, I learned that KeePass uses KDBX files as the password databases. (https://keepass.info/).

Oh ho ho! It worked! Now was the time to peruse the database . . .

![](/images/memlabs2/keepass_1.png)

Under Recycle Bin, I noticed the username of Flag!

![](/images/memlabs2/keepass_2.png)

Copying the password revealed: `flag{w0w_th1s_1s_Th3_SeC0nD_ST4g3_!!}`

## Flag 3

Now for the third flag . . . I hadn't checked internet browsers and there were a lot of chrome browsers open.

Something I learned recently - When you have browsers, there will be one parent process that represents opening the browser. Then, for each tab, a separate child process will be created! So what I wanted to focus on were the child processes (or childprocs). Based on `pstree`, there were five childprocs to be dumped.

I planned to use `strings`  and just browse through them for the keyword "password" or "passwd".

![](/images/memlabs2/Oneeternitylater.jpg)

I decided to turn my attention to browser artifacts. There's already a module for IE history but what about Chrome? I finally figured out that I could dump the Chrome history file and parse it using the free BrowsingHistoryView tool.

![](/images/memlabs2/filescan_3.png)

![](/images/memlabs2/dumpfiles_2.png)

Most sites were simply Google searches or blog sites. However, there was one that stood out as highlighted below.

![](/images/memlabs2/browsinghistoryview.png)

![](/images/memlabs2/mega_link.png)

I tried unzipping the downloaded file but got an unusual error:

![](/images/memlabs2/unzip_important_1.png)

![](/images/memlabs2/unzip_important2.png)

That error simply meant I had to use 7z.

![](/images/memlabs2/7z.png)

Using CyberChef made it easy to calculate the SHA1 of the previous lab's third flag.

![](/images/memlabs2/sha1.png)

Using that hash, I was able to find the third and final flag:

![](/images/memlabs2/important_png.png)

## Conclusion
So the three flags are
* `flag{w3lc0m3_T0_$T4g3_!_Of_L4B_2}` - from the environment variable
* `flag{w0w_th1s_1s_Th3_SeC0nD_ST4g3_!!}` - from the KeePass database
* `flag{oK_So_Now_St4g3_3_is_DoNE!!}` - from the Chrome browsing history
