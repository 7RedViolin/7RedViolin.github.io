---
layout: page
title: "macOS - What is SIP?"
date: 2021-08-05 13:00:00 -0000
tags: macOS forensics howto
intro: What is SIP? A quick dive into the security integrity protection feature introduced back in 10.X that helps keep Apple machines safe from unsigned code.
---
SIP (system integrity protection) is used on macOS to prevent unsigned or unknown code from executing freely. For troubleshooting or testing purposes, you can disable SIP altogether by booting into recovery mode. Of course, once you're done testing, it's a best practice to turn SIP back on.

1. Boot into Recovery Mode
    - Press and hold `CMD + R` when booting up the machine until the Apple logo appears.
    - If you're on a VM, it may be easier to run the following commands in the Terminal
    ```
    sudo nvram "recovery-boot-mode=unused"
    sudo reboot recovery
    ```
2. Once the machine has started, you'll see the Recovery/Installer page. From the top menu bar, click `Utilities > Terminal`
3. Run the commands 
```
csrutil disable
reboot
```
4. To verify if SIP is enabled/disabled run the command 
```
csrutil status
```

Note: To turn SIP back on, follow the above steps but run `csrutil enable` instead.