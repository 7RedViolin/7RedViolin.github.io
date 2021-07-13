---
layout: page
title: macOS Forensics
---
With the rise of macOS-heavy environments, I realized my limited knowledge of the inner workings of Apple devices. All my experience thus far has been strictly with Windows machines - and since there is minimal, if any, overlap between the two, I'm at a severe disadvantage when investigating macOS EDR data. 

To document my learning, I decided to start a blog series of the different forensic artifacts and other macOS-specific tidbits including acquisition methods, troubleshooting, and malware.

## Posts

<div>
    <ul>
        {%- for post in site.tags.macOS -%}
            <li><a href="{{post.url}}">{{ post.title }}</a></li>
        {%- endfor -%}
    </ul>
</div>

## Terms and Definitions
- **dylib**  
Short for `dynamic library`, a dylib is a shared resource similar to a Windows DLL file.
- **fseventsd**  
The process responsible for monitoring any file system events. You can kinda think of this as an MFT record keeper in Windows language.
- **Gatekeeper**  
A security feature starting in Catalina (i think???) that prevents unknown/unsigned software from running.
- **KEXT**  
Short for `kernel extension`, a KEXT file can be used to access the kernel and read data such as memory.
- **Launch Agent**
- **Launch Daemon**
- **launchd**
- **mach-o binary**  
The format of an standalone executable on a macOS device.
- **osascript**
- **plist**  
Short for `property list` contains information similar to registry hives on Windows machines.
- **SIP**