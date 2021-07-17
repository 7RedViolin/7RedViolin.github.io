---
layout: page
title: "macOS Memory Acquisition"
date: 2021-07-16 13:00:00 -0000
tags: macOS forensics memory howto
intro: How to dump memory from macOS devices using OSXPmem.
---
Unlike Windows, collecting macOS memory is more than just double-clicking on an executable. From my testing, you need to verify Terminal has full disk access and the app/kext you use is both owned by root:wheel and is not under quarantine.

1. Verify Terminal has full disk access.  
This can be done by going into `Settings > Security & Privacy > Privacy` and under `Full Disk Access` the Terminal app is checked.
2. With macOS Catalina (10.15.X), I was still able to use the OSXPMem version 3.9. Make sure the OSXPMem app is on an external drive with enough free space to capture all the RAM.
3. In the target machine's Terminal, change to the root account using `sudo su`.
4. Change the owner of the OSXPMem to root:wheel using the command `chown -R root:wheel osxpmem.app`
5. To bypass SIP (system integrity protection), remove the quarantine extended attribute on the osxpmem.app folder and all its contents using the command `xattr -r -d com.apple.quarantine osxpmem.app`
6. To dump memory into a raw format that can be used by Volatility, run the command `sudo osxpmem.app/osxpmem -o [location/name of output].raw --format raw`

Note: You may get a pop saying the OSXPMem application was blocked. You'll need to go into `Settings > Security & Privacy` and under `General`, make sure you've allowed the block application to run. Afterwards, run step 6 again.