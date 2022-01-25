---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Kerberoasting on an Open Fire"
date: 2022-01-25 21:00:00 -0500
tags: ctf kringlecon-2021 active-directory
intro: No MFA, weak passwords, and shell escapes - what could possibly go wrong?
---

## Objective: Kerberoasting on an Open Fire
> Obtain the secret sleigh research document from a host on the Elf University domain. What is the first secret ingredient Santa urges each elf and reindeer to consider for a wonderful holiday season? Start by registering as a student on the ElfU Portal.

## Summary

This is probably the longest walkthrough I've created as this challenge had many steps. With that in mind, here's a TL;DR in case you just want the high-level stuff.

1. Escape Python program
2. Escape Python shell
3. Enumerate network
4. Enumerate open shares
5. Enumerate accounts
6. Get user SPNs
7. Generate wordlist and crack password hash
8. Escalate privilege and move laterally
9. Add basic user account to privileged AD group
10. Access restricted share and exfiltrate data

## Details

Once I registered for the ELFU Portal, I got credentials and SSH instructions to access the grading system:

![Grading System](/images/kringlecon2021/kerberoast_1.png)

If I entered anything except `1` or `e`, the page was just reloaded.

![Input 1](/images/kringlecon2021/kerberoast_2.png)

![Input e](/images/kringlecon2021/kerberoast_3.png)

So I wondered if there was a way to escape the program - either via SSH commands when authenticating or a special input once the page was loaded. I went down the rabbit hole of SSH first but without any luck. (But I did learn a lot about SSH escape codes and flags from this [SANS article](https://www.sans.org/blog/using-the-ssh-konami-code-ssh-control-sequences/) and this [SSH.org article](https://www.ssh.com/academy/ssh/command#executing-remote-commands-on-the-server).) 

Next, I tred to escape the program using a special input once the page was loaded. Hints on Discord mentioned the page was running python so I tried `quit()`, `eval(quit())`, `exit()`, and other similar methods but these attempts either ended the session or just reloaded the page. 

The secret was actually the escape sequence CTRL+D to force the end-of-file (EOF) signal. CT +C didn't interrupt the script but CTRL+D worked like a charm and dropped me into a Python shell.

![CTRL + D](/images/kringlecon2021/kerberoast_4.png)

Mark Baggett demonstrated several different methods to escape a Python shell on [YouTube](https://www.youtube.com/watch?v=ZVx2Sxl3B9c) but I kept it simple by running `os.system(/bin/bash)`

![Dropping into a Bash shell](/images/kringlecon2021/kerberoast_5.png)

Once I was on the internal network as an authenticated user, I was ready to start prepping to attack AD! (Side note: I referenced Chris Davis' [YouTube video](https://www.youtube.com/watch?v=iMh8FTzepU4) on attacking AD and Michael Koczwara's [writeup](https://michaelkoczwara.medium.com/active-directory-penetration-testing-thm-vulnnet-roasted-ec056a249f3f) on ASEP roasting and Kerberoasting a lot throughout this process.) 

My first step was to identify all the routes and recently resolved IPs. 

![route output](/images/kringlecon2021/kerberoast_6.png)

![arp output](/images/kringlecon2021/kerberoast_7.png)

According to the `route` output, my current subnet was pretty large: /16 or room for 65534 hosts. This would take way too long to scan the entire subnet. Instead, I used the output from `arp` to only target live hosts.

To do that, I saved the output of arp to a text file and formatted it to only include one IP per line:

![Formatting IP list](/images/kringlecon2021/kerberoast_8.png)

Then, I ran Nmap against that list to see what ports were open and what services were running on each host.

![Nmap run #1](/images/kringlecon2021/kerberoast_9.png)

Out of all of those hosts (and there were over 200), only one stood out as a Windows device with SMB open - SHARE30.

![SHARE30](/images/kringlecon2021/kerberoast_10.png)

Sometimes, admins don't lock down shares to specific users and leave it open to all authenticated accounts. In this case, I was able to enumerate shares and view the contents of `sysvol` (nothing interesting there but a couple empty directories) but the shares `elfu_svc_shr` and `research_dep` were locked down.

![Share enumeration](/images/kringlecon2021/kerberoast_11.png)

![Access to sysvol](/images/kringlecon2021/kerberoast_12.png)

![No access to these shares](/images/kringlecon2021/kerberoast_13.png)

The share `IPC$` caught my attention since that can be used to enumerate account names. Impacket has a nice little script called `lookupsid.py` that can do it if you just provide the user account to do the enumeration and the IP of the host with the open share.

![Impacket's lookupsid.py](/images/kringlecon2021/kerberoast_14.png)

After that script ran, I also formatted the output to only capture the user accounts minus the domain. This was so I could use the output with Impacket's GetUserSPNs.py script to capture ticket info that will include a user account's encrypted password.

![Impacket's GetUserSPNs.py](/images/kringlecon2021/kerberoast_15.png)

![Hash of elfu_svc account](/images/kringlecon2021/kerberoast_16.png)

Once I had a hash of elfu_svc's password, I needed to crack it. Earlier, one of the elves hinted that I could use CeWL (a Customer Word List generator) against the ELFU portal.

![CeWL output](/images/kringlecon2021/kerberoast_17.png)

With a wordlist in hand, I used Hashcat to crack the password.

![Hashcat parameters](/images/kringlecon2021/kerberoast_18.png)

![Hashcat output](/images/kringlecon2021/kerberoast_19.png)

I was then able to access the `elfu_svc_shr` with these new credentials and copy files to my current directory. I eventually discovered `Get-ProcessInfo.ps1` had password information. 

![Accessing elfu_svc_shr](/images/kringlecon2021/kerberoast_20.png)

![Copying the PowerShell script](/images/kringlecon2021/kerberoast_21.png)

![Contents of the PowerShell script](/images/kringlecon2021/kerberoast_22.png)

I suspected the remote_elf account had special privileges so I modified the PowerShell script to target DC01 (the name was discovered in the lookupsid.py output) and start a remote PowerShell session.

![Modifying the PowerShell script](/images/kringlecon2021/kerberoast_23.png)

![Running the modified PowerShell script](/images/kringlecon2021/kerberoast_24.png)

From here, I wanted to enumerate the AD groups. Remembering that my goal was to access the research_dep share, I was looking for a group with the name "research department" or similar.

![Enumerate AD groups](/images/kringlecon2021/kerberoast_25.png)

![Research Department AD group](/images/kringlecon2021/kerberoast_26.png)

Then, I needed to check if the remove_elf account could edit that Research Department group membership:

![Check permissions commands](/images/kringlecon2021/kerberoast_27.png)

![Check permissions results](/images/kringlecon2021/kerberoast_28.png)

Since I had `WriteDacl` access through the remote_elf account, I added my basic account (the one given when I first signed up) to the Research Department group.

![Add access commands](/images/kringlecon2021/kerberoast_29.png)

![Verify access added](/images/kringlecon2021/kerberoast_30.png)

![Add membership commands](/images/kringlecon2021/kerberoast_31.png)

![Verify membership added](/images/kringlecon2021/kerberoast_32.png)

Now I was ready to access the share so I exited the PowerShell session and initiated the `smbclient` to grab a copy of the file:

![Accessing the research_dep share](/images/kringlecon2021/kerberoast_33.png)

But dang it! It was in PDF format so I had to then move the copy off of the ELFU network and on to my own machine. This took some time to figure out but I realized if I could switch the default login shell (which was originally set to the grading Python script) to bash, I would be able to run SCP commands and pull the file down locally.

![Editing the default login shell](/images/kringlecon2021/kerberoast_34.png)

![Pulling the file locally via SCP](/images/kringlecon2021/kerberoast_35.png)

Opening up the PDF, it was clear the flag was `kindness`.

![Viewing the PDF](/images/kringlecon2021/kerberoast_36.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [SANS SSH info](https://www.sans.org/blog/using-the-ssh-konami-code-ssh-control-sequences)
- [SSH.org](https://www.ssh.com/academy/ssh/command#executing-remote-commands-on-the-server)
- Escaping Pythong Shells with Mark Baggett
- [Attacking AD with Chris Davis](https://www.youtube.com/watch?v=iMh8FTzepU4)
- [ASEP Roasting and Kerberoasting Walkthrough by Michael Koczwara](https://michaelkoczwara.medium.com/active-directory-penetration-testing-thm-vulnnet-roasted-ec056a249f3f)
- [Impacket's lookupsid.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/lookupsid.py)
- [Impacket's GetUserSPNs.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py)
- [CeWL documentation](https://github.com/digininja/CeWL)
- [Hashcat documentation](https://hashcat.net/hashcat/)
-[] PowerShell snippets from Chris Davis](https://github.com/chrisjd20/hhc21_powershell_snippets)
- [Default login shell documentation](https://linux.die.net/man/1/chsh)
- [SCP documentation](https://linux.die.net/man/1/scp)