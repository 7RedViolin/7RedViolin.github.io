---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Strace, Ltrace, Retrace"
date: 2022-01-11 21:00:00 -0600
tags: ctf kringlecon-2021 reverse-engineering linux
intro: When an ELF binary doesn't work as expected, how can we troubleshoot it?
---

Here's a writeup of another side quest that required some light reversing of an ELF binary.

## Side Quest: Linux Process Investigation

![Linux Process Investigation Objective](/images/kringlecon2021/strace_ltrace_retrace_1.png)

We're given an ELF binary that seems to be missing a registration file. No other errors are shown so we'll need to start tracing the process using a couple tools: `strace` and `ltrace`.

With `strace`, we can view the system calls. Special flags can filter the output but, to keep it basic, I ran it without any parameters.

![strace command](/images/kringlecon2021/strace_ltrace_retrace_2.png)

In the output, we can see the `openat` syscall for a `registration.json` file.

![strace output - openat](/images/kringlecon2021/strace_ltrace_retrace_3.png)

Just for kicks, I created an empty file named `registration.json` to see if it worked or if any useful errors could be found. But no such luck!

![Try #1](/images/kringlecon2021/strace_ltrace_retrace_4.png)

Syscalls can only get you so far so we'll need to pull out `ltrace` for more information. With `ltrace`, we can view library calls. From this initial run, we can see the `strstr` function comparing the file contents with the expected value (in this case, the keyword `Registration`).

![ltrace output - #1](/images/kringlecon2021/strace_ltrace_retrace_5.png)

Now it's just a process of running ltrace to see what values it expects and adding those values to the `registration.json` file.

![ltrace output - #2](/images/kringlecon2021/strace_ltrace_retrace_6.png)

![ltrace output - #3](/images/kringlecon2021/strace_ltrace_retrace_7.png)

![ltrace output - #4](/images/kringlecon2021/strace_ltrace_retrace_8.png)

Unfortunately, I wasn't able to get a screenshot of a successful run because, once you are able to run `make_the_candy`, ascii art starts to flow across the screen. However, to recap, the answer is to create the file `registration.json` with the contents
```
Registration:True
```

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
* [Strace man page](https://man7.org/linux/man-pages/man1/strace.1.html)
* [Ltrace man page](https://man7.org/linux/man-pages/man1/ltrace.1.html)
* [OpenAt Syscall](https://linux.die.net/man/2/openat)
* [StrStr Library Call](https://man7.org/linux/man-pages/man3/strstr.3.html)