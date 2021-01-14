---
layout: default
title: "KringleCon 3: French Hens WriteUp - Part 1"
date: 2021-01-13 21:00:00 -0600
---
# KringleCon 3: French Hens WriteUp - Part 1
![](/images/kringlecon2020_obj/logo.PNG)
## Introduction
During the holiday break, I spent quite a few evenings working through the 2020 Holiday Hack Challenge (aka KringleCon 3: French Hens). If you aren't familiar with the Holiday Hack Challenges, I highly recommend checking them out. This and past CTFs are available year-round for review and provide ways to learn new skills ranging from threat hunting to web exploits to steganography. The problems really run the gamut of cyber topics!

Now, on to this year's challenge! This write up will be broken into two parts: Objectives and Side Quests. This part will be focused on objectives and will include not only solutions but also references I used to solve the problems. Unfortunately, I didn’t make it through all the available problems but what I did complete is outlined here. Below is the narrative I unlocked for solving 10 ½ out of the possible 11 objectives.  
![Narrative poem](/images/kringlecon2020_obj/narrative_poem.png)  
## Objectives & Walkthroughs
### Objective 1: Uncover Santa's Gift List
#### Description
There is a photo of Santa’s desk on that billboard with his personal gift list. What gift is Santa planning on getting Josh Wright for the holidays? Talk to Jingle Ringford at the bottom of the mountain for advice.
#### Solution
Before I made my way to the castle, I saw the billboard advertising the North Pole on the highway and grabbed a copy of the image.  
![Image of Santa's desk](/images/kringlecon2020_obj/kringlecon2020_obj/obj1_original.png)  
When I zoomed into the image, I saw the gift list was swirled to be unreadable. Now was the time to pull out GIMP! If you haven’t heard of or used GIMP before, it’s a photo editing software similar to Photoshop but free.  

I put a blue dot in the center of the image before I started cropping the image to make sure I kept the cropping fairly centered. If the cropped image was off-center, the “unswirling” wouldn’t work.  
![Revealed Santa's gift list](/images/kringlecon2020_obj/obj1_post_swirl.png)  
Using the Whirl & Pinch feature, I was able to adjust the whirl to run counterclockwise (negatively). If I had been able to center the image better, the “unswirling” would have been more successful.  

Answer: **Proxmark**

#### References
https://www.gimp.org/  
https://docs.gimp.org/2.4/en/plug-in-whirl-pinch.html

### Objective 2: Investigate S3 Bucket
#### Description
When you unwrap the over-wrapped file, what text string is inside the package? Talk to Shinny Upatree in front of the castle for hints on this challenge.
#### Solution
![S3 Bucket Site](/images/kringlecon2020_obj/obj2_scene.png)  
For this puzzle, I started by finding a “good” bucket name . . .  
![](/images/kringlecon2020_obj/obj2_opening.png)  
After a short brainstorming session, I came up with the following list:  
![A good bucket name](/images/kringlecon2020_obj/obj2_options.png)  
Testing these theories, I saw wrapper3000 came back positive!  
![Bucket search results](/images/kringlecon2020_obj/obj2_bucket_finder.png)  
Downloading the file showed a base64 encoded string.  
![](/images/kringlecon2020_obj/obj2_expand1.png)  
Unfortunately, the decoded string didn’t give me an ASCII file. However, I used the file command to determine the type of document.  
![](/images/kringlecon2020_obj/obj2_expand2.png)  
![](/images/kringlecon2020_obj/obj2_expand3.png)  
Now I had to do some google-fu and see how to extract this file over and over.  
![](/images/kringlecon2020_obj/obj2_expand4.png)  
![](/images/kringlecon2020_obj/obj2_expand6.png)  
![](/images/kringlecon2020_obj/obj2_expand7.png)  
![](/images/kringlecon2020_obj/obj2_expand8.png)  
Eventually, an ASCII file appeared!  
![](/images/kringlecon2020_obj/obj2_expand9.png)  

Answer: **North Pole: The Frostiest Place on Earth**

#### References
https://linuxhint.com/bash_base64_encode_decode/  
https://linux.die.net/man/1/unzip  
https://www.geeksforgeeks.org/bzip2-command-in-linux-with-examples/  
https://linux.die.net/man/1/tar  
https://linux.die.net/man/1/xz  
https://linux.die.net/man/1/uncompress  
https://www.systutorials.com/docs/linux/man/1-xxd/  

### Objective 3: Point-Of-Sale Password Recovery
#### Description
Help Sugarplum Mary in the Courtyard find the supervisor password for the point-of-sale terminal. What’s the password?

#### Solution
![](/images/kringlecon2020_obj/obj3_scene.png)  
Clicking on the “Santa Shop” computer gave me an EXE file. But I thought it was supposed to be an ASAR file? This was slightly confusing.  

But all the hints recommended extracting the EXE so it was time to reference 7zip.  
![](/images/kringlecon2020_obj/obj3_expand1.png)  
Listing the extracted items, I still didn’t see an ASAR file.  But there was another archive so I extracted that as well.  
![](/images/kringlecon2020_obj/obj3_ls1.png)  
![](/images/kringlecon2020_obj/obj3_expand2.png)  
Running ls again, I saw a couple folders I could check.  
![](/images/kringlecon2020_obj/obj3_ls2.png)  
And the ASAR file was located in the resources folder.  
![](/images/kringlecon2020_obj/obj3_ls3.png)  
Rather than poke through all the scripts, I chose to open the README.md in the hopes it would give me a hint.  
![](/images/kringlecon2020_obj/obj3_readme.png)  

Answer: **Santapass**

#### References
https://medium.com/how-to-electron/how-to-get-source-code-of-any-electron-application-cbb5c7726c37

### Objective 4: Operate the Santavator
#### Description
Talk to Pepper Minstix in the entryway to get some hints about the Santavator.

#### Solution
![](/images/kringlecon2020_obj/obj4_scene1.png)  
![](/images/kringlecon2020_obj/obj4_scene2.png)  
To solve the puzzle, I used the objects found around the castle to access the second floor.  
![](/images/kringlecon2020_obj/obj4_tools.png)  
![](/images/kringlecon2020_obj/obj4_tools2.png)  
Opening the circuit board, I was able to turn on the green light using the configuration below and access the 2nd floor.  
![](/images/kringlecon2020_obj/obj4_config1.png)  
However, I wanted to be able to access all the other floors, too. A hint suggested a more “hacky” approach so I reviewed the source code.  

In the app.js file, I could force the laser color to be red by changing the particle.color variable from 3 to 0.  
![](/images/kringlecon2020_obj/obj4_code.png)  
![](/images/kringlecon2020_obj/obj4_config2.png)  
After figuring out the “hack”, I did come across the rest of the pieces and set up the bulbs accordingly.  
![](/images/kringlecon2020_obj/obj4_config3.png)  

### Objective 5: Open HID Lock
#### Description
Open the HID lock in the Workshop. Talk to Bushy Evergreen near the talk tracks for hints on the challenge. You may also visit Fitzy Shortstack in the kitchen for tips.

#### Solution
![](/images/kringlecon2020_obj/obj5_scene1.png)  
![](/images/kringlecon2020_obj/obj5_scene2.png)  
I got the Proxmark device and went around the castle to different elves and captured their tag info.  

The first elf I targeted was Bow Ninecandle.  
![](/images/kringlecon2020_obj/obj5_elf.png)  
![](/images/kringlecon2020_obj/obj5_hid1.png)  
Once I found a code, I went to the locked door in the Workshop and used the Proxmark to trick the card reader.  
![](/images/kringlecon2020_obj/obj5_hid2.png)  
This got me into the locked workshop room!  
![](/images/kringlecon2020_obj/obj5_lights.png)  
At the end of the room, there were some spooky floating lights that, once I reached them, allowed me to magically become Santa in the Entry!  
![](/images/kringlecon2020_obj/obj5_santa.png)  

### Objective 6: Splunk Challenge
#### Description
Access the Splunk terminal in the Great Room. What is the name of the adversary group that Santa feared would attack KringleCon?  
![](/images/kringlecon2020_obj/obj6_scene.png)  
Now that I became “Santa”, I had access to the Splunk computer in the Great Room without any issues. Before I could answer the objective question on adversary groups, I had to go through seven “training” questions.  

The first few questions were answered simply by running the query `| tstats count where index=* by index` as shown below.  
![](/images/kringlecon2020_obj/obj6_splunk1.png)  
**Training Question #1: How many distinct MITRE ATT&CK techniques did Alice emulate?**

Since the first question was about distinct techniques, it was important to know the naming standard is “Technique.SubTechnique-OS”. That makes the total **13**.

**Training Question #2: What are the names of the two indexes that contain the results of emulating Enterprise ATT&CK technique 1059.003? (put them in alphabetical order and separate them with a space)**

For the second question, I was looking for indices that start with “1059.003”. Just scrolling through the results from the query in question #1, I could tell the answer was **t1059.003-main t1059.003-win**

**Training Question #3: One technique that Santa had us simulate deals with ‘system information discovery’. What is the full name of the registry key that is queried to determine the MachineGUID?**

The third question wasn’t answered in the Splunk portal but rather the Atomic Red Team GitHub repo. There is a yaml file in the repo for T1082 with all the details. At the bottom was the reg key I was looking for: **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography**

**Training Question #4: According to events recorded by the Splunk Attack Range, when was the first OSTAP related atomic test executed? (Please provide the alphanumeric UTC timestamp.)**

The fourth question required that I check the catch-all “attack” index for the keyword “OSTAP”. I saw only six events were returned so it was easy to compare these few events and figure out the earlier timestamp: **2020-11-30T17:44:15Z**

**Training Question #5: One Atomic Red Team test executed by the Attack Range makes use of an open source package authored by frgnca on GitHub. According to Sysmon (Event Code 1) events in Splunk, what was the ProcessId associated with the first use of this component?**

The fifth question was a little more complex – first, I looked up the developer on GitHub. The only repository that made sense to me was the AudioDeviceCmdlets.  
![](/images/kringlecon2020_obj/obj6_github1.png)  
Reading through the description, the commands to watch were Get-AudioDevice, Set-AudioDevice, and Write-Audio-Device.  

Back to Splunk, I ran a query for that activity and found two hits.  
![](/images/kringlecon2020_obj/obj6_splunk2.png)  
![](/images/kringlecon2020_obj/obj6_splunk3.png)  
To pivot, I needed to look at the T1123 index and filter to powershell.exe and Sysmon event ID 1 (process started).  

I was really confused for quite a while – ProcessID for all the results was 2263 but that answer was not accepted. It wasn’t until I started poking into the event details that I found two very similar field names: ProcessID and ProcessId. What’s the difference? I had (and still have) no clue yet but I was able to determine the correct answer (3648) with the following query:  
`index=t1123* process_exec=powershell.exe EventCode=1 CommandLine="\"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe\" &amp; {powershell.exe -Command WindowsAudioDevice-Powershell-Cmdlet}"`  
**Training Question #6: Alice ran a simulation of an attacker abusing Windows registry run keys. This technique leveraged a multi-line batch file that was also used by a few other techniques. What is the final command of this multi-line batch file used as part of this simulation?**

As with the previous question, problem #6 required me to use the attack index and search for the keyword “reg” or “run”. I found the technique 1547 which led to the index t1547*.  
![](/images/kringlecon2020_obj/obj6_splunk4.png)  
The query `index=t1547*` brought up over 1,000 events so, to pare it down, I filtered to only Sysmon event ID 1 (process started) and the keyword “bat”. The filtered query came back with only four events.  
![](/images/kringlecon2020_obj/obj6_splunk5.png)  
I looked at the statistics of the command lines and noticed one referenced the bat file in a folder called “Atomic Red Team” . . . I was off to check GitHub!  
![](/images/kringlecon2020_obj/obj6_splunk6.png)  
Inside the T1547.001 scr directory was a batstartup.bat file as expected.  
![](/images/kringlecon2020_obj/obj6_github2.png)  
![](/images/kringlecon2020_obj/obj6_splunk7.png)  
But was the answer really “echo”?  
![](/images/kringlecon2020_obj/obj6_error.png)  
In retrospect, that made sense given the clue specifically mentioned a “multi-line” batch file. If this wasn’t the target, what other bat files were in references in Splunk? I ran the query `index=* "bat" TargetFilename!= "C:\\AtomicRedTeam\\tmp\\atomic-red-team-local-master\\atomics\\T1547.001\\src\\batstartup.bat"` and saw what other target files were out there that possibly made sense.  
![](/images/kringlecon2020_obj/obj6_splunk8.png)  
A lot! I was wearing out and didn’t want to use up too many more brain cells trying to be smart so, by process of elimination, I went down the list and researched each bat file.  

After perusing all of the bat files, I was at a loss – none of them were related to T1547.001 – What was I missing? I scanned the docs again and noticed only the Discovery.bat files made any reference to registry keys.  
![](/images/kringlecon2020_obj/obj6_yaml.png)  
Could it be that simple and yet complex? I checked the last command in the bat file and entered **quser** it with crossed fingers . . .  

Success!  

**Training Question #7: According to x509 certificate events captured by Zeek (formerly Bro), what is the serial number of the TLS certificate assigned to the Windows domain controller in the attack range?**

The last question required some network knowledge. I noticed the keywords “x509”, “certificate”, “serial number”, and “domain controller”. To get a sense of what the logs contained, I used the query `index=* sourcetype=bro* "x509"` but that didn’t help at ALL! I didn’t see any hostnames, serial numbers, or certificate names like I expected . . .  
![](/images/kringlecon2020_obj/obj6_splunk9.png)  
So I tried the keyword “serial” instead and boom! This is what I was expecting:  
![](/images/kringlecon2020_obj/obj6_splunk10.png)  
The field I was looking for was certificate.serial: **55FCEEBB21270D9249E86F4B9DC7AA60**  

The final challenge question required a string be decoded using a keyword mentioned in a Splunk talk:  
![](/images/kringlecon2020_obj/obj6_final_clue.png)  
![](/images/kringlecon2020_obj/obj6_answer.png)  

Answer: **The Lollipop Guild**

#### References
https://www.youtube.com/watch?v=qbIhHhRKQCw  
https://www.youtube.com/watch?v=RxVgEFt08kU

### Objective 7: Solve the Sleigh’s CAN-D-BUS Problem
#### Description
Jack Frost is somehow inserting malicious messages onto the sleigh’s CAN-D bus. We need you to exclude the malicious messages and no others to fix the sleigh. Visit the NetWars room on the roof and talk to Wunorse Openslae for hits.
#### Solution
![](/images/kringlecon2020_obj/obj7_scene.png)  
This required a lot of trial and error but I soon figured out the following:  

| Event ID | Event Data | Meaning |
| --- | ----------- | --- |
| 19B | 000000000000 | Lock |
| 19B | 00000F000000 | Unlock |
| 02A | 00FF00 | Start |
| 02A | 0000FF | Stop |
| 019 | Any | Steering |
| 080 | Any | Braking |
| 188 | Any | Acceleration |
| 244 | Any | Speed |

As a side note, I was also able to determine the accelerator and brakes had a limit of 0 to 100 (0 to 64 in hex). Steering had a range of -50 to +50 (FFFFFFCE to 32 in hex). Speed ranged from 0 to 9999 (0 to 270F in hex).

Using these notes, I was able to exclude the noise with the filters below.  
![](/images/kringlecon2020_obj/obj7_answer.png)  

#### References
https://www.youtube.com/watch?v=96u-uHRBI0I

### Objective 8: Broken Tag Generator
#### Description
Help Noel Boetie fix the Tag Generator in the Wrapping Room. What value is the environment variable GREETZ? Talk to Holly Evergreen in the kitchen for help with this.

#### Solution
![](/images/kringlecon2020_obj/obj8_scene.png)  
First, I peeked at the app.js code. The only control I had over the site was uploading files and entering text to print on the tag. I noticed the script references a `/image?id=${id}` query when a file was uploaded. Could this be used to traverse the directory on the host?  
![](/images/kringlecon2020_obj/obj8_code1.png)  
I initially tried going to `../../../../../etc/profile` to see if it worked . . . Which I was able to verify by decoding the base646 encoded string that was returned.  
![](/images/kringlecon2020_obj/obj8_directory1.png)  
![](/images/kringlecon2020_obj/obj8_cyberchef1.png)  
Now based on my Google searching, `/etc/environment` should have given me a list of environment variables . . . but no success.  
![](/images/kringlecon2020_obj/obj8_directory2.png)  
Eventually, I found a StackOverflow thread mentioning environment variables contained in process folders based on process ID (see references below for link). Why had I never heard of this before? I decided I would just have to go down the number line until I got a hit. However, it didn’t take nearly as long as I expected.  
![](/images/kringlecon2020_obj/obj8_directory3.png)  
![](/images/kringlecon2020_obj/obj8_cyberchef2.png)  

Answer: **JackFrostWasHere**

#### References
https://stackoverflow.com/questions/532155/linux-where-are-environment-variables-stored

### Objective 9: ARP Shenanigans
#### Description
Go to the NetWars room on the roof and help Alabaster Snowball get access back to a host using ARP. Retrieve the document at /NORTH_POLE_Land_Use_Board_Meeting_Minutes.txt. Who recused herself from the vote described on the document?

#### Solution
![](/images/kringlecon2020_obj/obj9_scene.png)  
In this challenge, a machine (10.6.6.35) had been infected with some sort of malware and was “inaccessible”. It was my job to gain access and read the text file mentioned in the objective from a random host on the same network as the infected machine.  

First, I ran the command tcpdump -nni etho0 to see what traffic was coming from the infected host.  
![](/images/kringlecon2020_obj/obj9_listener.png)  
It appeared that the infected host was searching for a machine with the IP 10.6.6.53. This implies a man-in-the-middle (MitM) attack was on the agenda for this challenge.  

One of the hints mentioned pre-baked scripts that could help located in the /home/guest/scripts folder.  
![](/images/kringlecon2020_obj/obj9_py_scripts.png)  
To customize the arp_resp.py script, I needed the following information:  
- My current MAC address
- IP address I want to spoof
- Target/Destination IP address
- Target/Destination MAC address

To get the target MAC address, I referenced the arp table as shown below.  
![](/images/kringlecon2020_obj/obj9_get_mac.png)  
Once I got my arp_script.py configured as shown below, I was able send a spoofed ARP response. This caused the infected machine to send out a DNS request to the domain “ftp.osuol.org”.  
![](/images/kringlecon2020_obj/obj9_arp_py.png)  
![](/images/kringlecon2020_obj/obj9_dns_request.png)  
On to configure the dns_resp.py script!  
![](/images/kringlecon2020_obj/obj9_dns_py.png)  
The above configuration took a LOT of trial and error but eventually I got the right settings and noticed the infected machine followed the DNS request with connection attempts to port 80. To capture what was being requested, I opened another terminal window and stood up a webserver.  
![](/images/kringlecon2020_obj/obj9_http_request.png)  
![](/images/kringlecon2020_obj/obj9_http_get.png)  
Then I could see the request was for some sort of deb file in a specific folder path.  

I could have created my own deb or I could have repurpose one of the existing deb files in the ~/debs folder. I decided to work smarter not harder and chose the latter option.  
![](/images/kringlecon2020_obj/obj9_debs.png)  
I was able to repurpose the netcat deb file but creating the payload required trial and error. I attempted a reverse shell using bash and netcat but with no success. Eventually, I was able to get socat working.  
![](/images/kringlecon2020_obj/obj9_payload1.png)  
![](/images/kringlecon2020_obj/obj9_payload2.png)  
Once the python scripts were adjusted and the deb file configured, I was ready to kick everything off! I ended up with four terminals as shown below. In the last terminal, I used socat to connect to the infected machine.  
![](/images/kringlecon2020_obj/obj9_window1.png)  
![](/images/kringlecon2020_obj/obj9_window2.png)  
![](/images/kringlecon2020_obj/obj9_window3.png)  
![](/images/kringlecon2020_obj/obj9_window4.png)  
When using the cat command, I was only able to view the very tail end of the meeting minutes text file. It took some trial and error but I eventually ended up using the head command repeatedly and incrementing returned lines by 5 or 10. Below are some screenshots of the meeting minutes throughout the course of my iterations. The answer can be found in the second screenshot.  
![](/images/kringlecon2020_obj/obj9_answer1.png)  
![](/images/kringlecon2020_obj/obj9_answer2.png)  
![](/images/kringlecon2020_obj/obj9_answer3.png)  

Answer: **Tanta Kringle**

#### References
https://www.cloudshark.org/captures/e4d6ea732135  
https://www.cloudshark.org/captures/56802b91286a  
https://thepacketgeek.com/scapy/building-network-tools/part-09/  
https://www.cs.dartmouth.edu/~sergey/netreads/local/reliable-dns-spoofing-with-python-scapy-nfqueue.html  
http://www.wannescolman.be/?p=98  
https://www.netsparker.com/blog/web-security/understanding-reverse-shells/  
https://blog.travismclarke.com/post/socat-tutorial/#:~:text=Socat%20is%20a%20command%20line,and%20transfers%20data%20between%20them  

### Objective 10: Defeat Fingerprint Sensor
#### Description
Bypass the Santavator fingerprint sensor. Enter Santa’s office without Santa’s fingerprint.

#### Solution
For this problem, I went back to the Santavator JavaScript and noticed it checked if the user had the “beSanta” token. The solution was simply deleting the highlighted section from the code below.  
![](/images/kringlecon2020_obj/obj10_code.png)  

### Objective 11a: Naughty/Nice List with Blockchain Investigation Part 1
#### Description
Description
Even though the chunk of the blockchain that you have ends with block 129996, can you predict the nonce for block 130000? Talk to Tangle Coalbox in the Speaker UNpreparedness Room for tips on prediction and Tinsel Upatree for more tips and tools. (Enter just the 16-character hex value of the nonce)

#### Solution
![](/images/kringlecon2020_obj/obj11_scene.png)
Opening the blockchain.dat file showed the data was definitely not ASCII.

This required the naughty_nice.py script to be adjusted to read and output the file into human-readable text. The bottom half the script had a section I could uncomment to get the necessary data as shown below.  
![](/images/kringlecon2020_obj/obj11_naughty_nice_py.png)  
I then used grep and cut to pull out all the nonces.  
![](/images/kringlecon2020_obj/obj11_get_nonces.png)  
![](/images/kringlecon2020_obj/obj11_read_nonces.png)  
Next, I needed to find a Mersenne twist script that could predict the next values. Even though the KringleCon speaker Tom Liston created his own script, fellow problem solvers on Discord also suggested kmyk’s Github script. I chose the latter since it was easier to wrap my brain around.  

I installed the mt19937predict script and used the C++ test outlined on the readme file to make sure the script was working properly. However, I kept getting the error that “contextlib.suppress” could not be found. After some trial and error, I was able to comment out the troublesome piece of code and use a try-except statement instead as shown below:  
![](/images/kringlecon2020_obj/obj11_mt19937_edit.png)  
This worked beautiful and then it was time to fix up the Naughty Nice nonces. The script only accepted 32-bit unsigned integers. So, rather than change the logic in the script, I decided to convert the hex nonce values using this script:  
![](/images/kringlecon2020_obj/obj11_nonce_parser.png)  
![](/images/kringlecon2020_obj/obj11_read_nonces_32bit.png)  
Now, to find the answer, I used the last 624 entries to predict future nonces.  
![](/images/kringlecon2020_obj/obj11_tail_nonces.png)  
![](/images/kringlecon2020_obj/obj11_predict_nonces.png)  
![](/images/kringlecon2020_obj/obj11_final_results.png)  
Since the last known entry was 129996 and the answer was to be the 130000th entry, I needed to skip down to the seventh and eighth lines as highlighted above.  

Based on Endianness, I also needed to reverse the order of the pair of numbers then convert to hex to get the expected answer.  
![](/images/kringlecon2020_obj/obj11_hex_conversion.png)  

Answer: **57066318f32f729d**

#### References
https://www.youtube.com/watch?v=reKsZ8E44vw&t=351s  
https://www.youtube.com/watch?v=Jo5Nlbqd-Vg  
https://github.com/tliston/mt19937  
https://github.com/kmyk/mersenne-twister-predictor  
https://stackoverflow.com/questions/209513/convert-hex-string-to-int-in-python  
https://www.w3schools.com/python/python_try_except.asp  
