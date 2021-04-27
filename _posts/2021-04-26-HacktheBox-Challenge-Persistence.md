---
layout: default
title: "Ransomware Thoughts"
date: 2021-04-26 13:00:00 -0000
---

# HacktheBox Challenge: Persistence

I recently got access to retired Hack the Box challenges and decided to provide write-ups as well as explanations of the forensics concepts behind the challenge. This is the first post in what will hopefully become a series on DFIR concepts.

Shout-out to ShaktiCon for the HtB voucher after competing in their CTF earlier this month! 

## Background

Persistence: You've probably already guessed the defintion given the context. This is the method used by legitimate software (or malware) to _persist_ on a machine and continues to run even after a restart/shutdown.

This way, even if you successfully remove the malicious file(s) but the persistence mechanism isn't deleted as well, the machine can continue to be re-infected.

On a Windows machine, there are several "go-to" methods common not only for legitimate software like Windows Updates but also malware. Below is a short list of the most common methods but there's a much more complete list has been curated by [Hexacorn](https://www.hexacorn.com/blog/2017/01/28/beyond-good-ol-run-key-all-parts/). 

1. Run Registry Keys  
For everything that exists on a Windows machine, there's almost always a related registry key. You can think of the registry as the DNA of the Windows OS. When looking for persistence, there are `run` and `runonce` keys that automatically start programs or scripts either repeatedly or a single instance.  
    - At machine boot
        - HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
        - HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
    - At user logon
        - HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
        - HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce

2. Scheduled Tasks  
Another avenue for persistence is scheduled tasks. These can be more flexible than registry keys since the trigger to start a program or script can range from a schedule (e.g. ever X hours) to the creation of a specific event in the Windows Event Log to lock/unlock status.   
There is both a GUI view via the Task Scheduler app and via the command line tool `schtasks`.

3. Services  
Depending on how the program or script is configured to work, a service can also be created to run either at boot, directly after boot, or manually.   
These can be viewed via the Services app or via the PowerShell command `Get-Service`

## HtB Challenge: Persistence

### Description
> We're noticing some strange connections from a critical PC that can't be replaced. We've run an AV scan to delete the malicious files and rebooted the box, but the connections get re-established. We've taken a backup of some critical system files, can you help us figure out what's going on?

### Solution

We're given a file called `query` but without any extension. I tried viewing via Notepad++ but it was gibberish. The beginning of the file, however, made me suspect it was a registry dump by the first three characters.

![](/images/hackthebox/persistence1.png)

I was able to open it using Eric Zimmerman's Registry Explorer tool found [here](https://ericzimmerman.github.io/#!index.md).

Based on the name of the challenge and description of the problem, this sounds like it involves run keys as mentioned above.

![](/images/hackthebox/persistence2.png)

Under `Software > Microsoft > Windows > CurrentVersion > Run`, we can see the value `WindowsUpdate` referencing an unusual exe file. Based on the types of characters in the name, it looked base64-encoded so I threw it into CyberChef.

![](/images/hackthebox/persistence3.png)

This gave me the answer `HTB{1_C4n_kw3ry_4LR19h7}`

## References
- [Beyond Good Ol' Run Keys](https://www.hexacorn.com/blog/2017/01/28/beyond-good-ol-run-key-all-parts/)
- [Registry Explorer Tool](https://ericzimmerman.github.io/#!index.md)
- [SANS "Evidence Of" Poster](https://www.sans.org/security-resources/posters/windows-forensic-analysis/170/download)