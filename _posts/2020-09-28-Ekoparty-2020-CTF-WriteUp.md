---
layout: default
title: "Ekoparty 2020 CTF WriteUp"
date: 2020-09-28 13:00:00 -0000
---
# Ekoparty 2020 CTF WriteUp

## Overview

Last week, I decided to participate in the Ekoparty CTF. This was organized by an Argentina-based conference that hosts speakers, trainings, and CTFs each year with topics ranging from traditional Red/Blue Team to IoT and ICS. This was an opportunity to practice and learn more about reverse engineering and malware analysis.  

## C&C1 Challenge
>Goal: This is a network capture of a generic trojan sample. May you please tell us the IP address of the C&C? 

For this problem, I pulled out Wireshark to analyze the pcap. From the statistics below, I have two external IPs that are listed under both source and destination. However, 8.8.8.8 can be ignored since that is for Google DNS.

![C&C1 Wireshark statistics](/images/ekoparty_2020/cc1_1.png)

Answer: EKO{54.204.19.83}

## C&C4 Challenge
>Goal: A malware found in the wild is trying to connect to a C&C. Can we have the related IP address? 

Running strings against the ELF file, it doesn't take long to find the IP!

![C&C4 file output](/images/ekoparty_2020/cc4_1.png)

![C&C4 strings output](/images/ekoparty_2020/cc4_2.png)

Answer: EKO{37.49.224.224}

## ABCD Challenge
>Goal: What's the name of this famous malware? 

Unzipping and running the file command showed me this was a PE32 executable.

My experience reversing these types of files is limited but I decided to start with one of my favorite commands - "strings".

![ABCD strings output](/images/ekoparty_2020/abcd_2.png)

Scrolling through, I recognized a keyword - "ryuk". This is a well-known ransomware that has targeted enterprises since 2018 with great success at causing destruction.

![ABCD ryuk keyword 1](/images/ekoparty_2020/abcd_3.png)

![ABCD ryuk keyword 2](/images/ekoparty_2020/abcd_4.png)

Answer: EKO{ryuk}

## Exe Challenge
>Goal: A common hash function used to identify malware is SHA256. May you please tell us what is the value of the hash for this malware sample? (Format uppercase SHA256)

This was an easy challenge that used the commands sha256 sum and tr.

![Exe sha256 sum and tr output](/images/ekoparty_2020/exe_1.png)

Answer: EKO{EBA35B2CD54BAD60825F70FB121E324D559E7D9923B3A3583BB27DFD7E988D0C}

## Run Challenge
>Goal: There are some antivirus products that cannot detect the following malware samples. Can you name one of them? 

It took a moment to think this one through - how could I possibly test this malware against "all" antivirus products? And then I remembered VirusTotal. VirusTotal (also known as VT) is a free tool that can test IPs, URLs, and files against multiple antivirus products. Just be warned any files uploaded are considered open for public use and review so don't add any potentially sensitive files out there! 

After uploading the file, the analysis showed 63 out of 70 vendors detected the malware - I just needed to provide one of the seven that missed the malware.

![Run VT results 1](/images/ekoparty_2020/run_1.png)

![Run VT results 2](/images/ekoparty_2020/run_2.png)

Answer: EKO{Alibaba}

## Clop Challenge
>Goal: This is one of the most dangerous malware sample. Researchers usually protect these samples with a common password. Extract the file and you will find the answer inside the sample.

This problem took a bit of head knowledge - from experience, I know a common password  used  to zip malware is "infected".

![Clop unzip using "infected" password](/images/ekoparty_2020/clop_1.png)

From there, I used the file command to determine the type and the strings command to look for interesting words.

![Clop file and strings output](/images/ekoparty_2020/clop_2.png)

At the bottom of the file, I see the flag!

![Clop flag](/images/ekoparty_2020/clop_3.png)

Answer: EKO{1nf3ct3d}

## Cert Challenge
>Goal: A malicious technique used by bad actors is to sign binaries with stolen certifiates. This malware sample is signed by a Chinese company. The answer is the name of this company.

So there's two ways I could have gone about this - one was to upload/search the file on VirusTotal. The other option was to inspect the file manually. First, I'll show how I found it manually and then share how to do it the "easy" way. 

Running strings, I scrolled down to the bottom of the page and noticed Symantec was mentioned for timestamping. Below that, was a reference to VeriSign - and the company name "Beijing Qihu Technology Co., Ltd".

![Cert Symantec timestamping 1](/images/ekoparty_2020/cert_1.png)

![Cert Symantec timestamping 2](/images/ekoparty_2020/cert_2.png)

![Cert VeriSign](/images/ekoparty_2020/cert_3.png)

Now how to do this via VirusTotal? If the file was already uploaded, I could have searched by hash - md5, SHA1, or SHA256 will work. 

![Cert SHA256](/images/ekoparty_2020/cert_4.png)

This malware was already scanned so the Details section would tell me the signers.

![Cert VT Description](/images/ekoparty_2020/cert_5.png)

![Cert VT Details](/images/ekoparty_2020/cert_6.png)

And here again, Symantec, VeriSign, and Beijing Qihu Technology appeared. Since the clue specifically mentioned a Chinese company, the flag must be the Beijing option.

Answer: EKO{Beijing Qihu Technology Co., Ltd.}

## COVID19 Challenge
>Goal: This file was found on a COVID-19 related phishing campaign. May you find the secret inside the file?

This was a different attachment since it appeared to be an ASCII file rather than a PE32.

![COVID19 file](/images/ekoparty_2020/covid19_1.png)

Using strings showed what appeared to be Visual Basic (also known as VB) script.

![COVID19 strings output](/images/ekoparty_2020/covid19_2.png)

The variable str had a long list of parenthesis and numbers/letters - at the bottom, however, it became clear the letters and numbers weren't random.

![COVID19 VBA script](/images/ekoparty_2020/covid19_3.png)

First, the script removed all ")" characters from the str variable. Then, for each letter/number couple, it converted from hex to string. The very last line executed whatever has been hex encoded.

So, I mimicked the code using PowerShell and wrote the output to a file. Shoutout to Dr. Scripto for the PowerShell code to convert hex to ASCII!

![COVID19 PowerShell script](/images/ekoparty_2020/covid19_4.png)

Once decoded, I could tell the hex-encoded data did super bad stuff but the flag was very obvious:

![COVID19 flag](/images/ekoparty_2020/covid19_5.png)

Answer: EKO{super_infected}

## Fifty Challenge
> Goal: A top secret file has been encrypted by an infamous ransomware. Will you be able to retrieve the original content?

Going into this one, I noticed the file had the extension "no_more_ransomware"

![Fifty file output](/images/ekoparty_2020/fifty_1.png)

I didn't recognize the extension so I turned to my good and trusted friend Google. This led me to using the website ID Ransomware which allowed me to upload the file and learn there were two possibilities:

![Fifty rapid ransomware option](/images/ekoparty_2020/fifty_2.png)

![Fifty shade ransomware option](/images/ekoparty_2020/fifty_3.png)

Since the flag asks us to decrypt the file, I'm going to assume we're dealing with Troldesh/Shade.

Back to Google, Kaspersky announced a free decryptor available for download. This tool gave me a 28-page Word doc titled "TOP SECRET DOC". Instead of scrolling endlessly, I just searched for "EKO".

![Fifty keyword search](/images/ekoparty_2020/fifty_4.png)

Answer: EKO{R4nd0mw4r3}

## References 
- Ekoparty Conference https://www.ekoparty.org/en_US/aboutus
- Ryuk Malware https://www.crowdstrike.com/blog/big-game-hunting-with-ryuk-another-lucrative-targeted-ransomware/
- VirusTotal - https://www.virustotal.com/gui/
- Powershell Script (Hex to ASCII) https://devblogs.microsoft.com/scripting/convert-hexadecimal-to-ascii-using-powershell/
- ID Ransomware https://id-ransomware.malwarehunterteam.com/
- Kaspersky Troldesh Decryptor https://support.kaspersky.com/13059
