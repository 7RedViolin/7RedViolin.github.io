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
The process responsible for monitoring any file system events.
- **Gatekeeper**  
A security feature starting in Catalina (i think???) that prevents unknown/unsigned software from running.
- **KEXT**  
Short for `kernel extension`, a KEXT file can be used to access the kernel and read data such as memory. These are being deprecated in BigSur (macOS 11) in favor of system extensions. The logic behind the change is to limit kernel-level access.
- **Launch Agent**  
Apple's method for application persistence at the user level. Processes run via Launch Agents will run with the given user's permissions with the configurations and parameters definied in one of the following directories: `~/Library/LaunchAgents`, `/Library/LaunchAgents`, or `/System/Library/LaunchAgents`
- **Launch Daemon**
Apple's method for application peristence at the system level. Processes run via Launch Daemons will run with system-level permissions with the configurations and parameters defined in one of the following directories: `/Library/LaunchDaemons` or `/System/Library/LaunchDaemons`
- **launchd**
This is the root process that will always have a PID of 1. All future processes will be spawned from `launchd`.
- **mach-o binary**  
The format of an standalone executable on a macOS device.
- **osascript**
Similar to wscript or cscript on a Windows machine, osascript is used to run scripts and commonly abused by adversaries. Supported languages include X, Y, Z. 
- **plist**  
Short for `property list` contains information similar to registry hives on Windows machines. These files may or may not have the `.plist` extension but you can always identify them by the file header. They can also be XML or binary formatted. Native to macOS, you can use the command `plutil -p FILENAME` to view the contents.
- **SIP**  
Short for `system integrity protection`, this is used on macOS to prevent unsigned or unknown code from executing freely.
- **XProtect**  
A built-in type of antivirus that uses YARA rules to protect against known malicious files. The YARA rules are read only and can be found in `/System/Library/CoreServices/XProtect.bundle/Contents/Resources`. As a side note, updates to the YARA rules are managed by Apple but are not necessarily done at the same time as system updates.