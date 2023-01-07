---
layout: page
title: "KringleCon 5: Five Golden Rings WriteUp - Tolkien Ring"
date: 2023-01-25 21:00:00 -0500
tags: ctf kringlecon-2022 eventlogs pcap wireshark powershell suricata
intro: Digging through logs for evil
---

![](/images/kringlecon2022/tolkien_ring.png)

## Objective #1: Wireshark Practice
> Use the WireShark Phishing terminal in the Tolkien Ring to solve the mysteries around the suspicious PCAP. Get hints for this challenge by typing hint in the upper panel of the terminal

### Details

Note: All of these answers will be done via the Wireshark GUI. However, you could also solve this via tshark (aka terminal-based Wireshark)

#### Question 1
> There are objects in the PCAP file that can be exported by Wireshark and/or Tshark. What type of objects can be exported from this PCAP?

To see what can be exported, open `File > Export Objects` and test each option. Only `HTTP` will have a list of available exports.

#### Question 2
> What is the file name of the largest file we can export?

By opening `File > Export Objects > HTTP`, the list can be sorted by size and show `app.php` is the largest file clocking in at 808 kB.

#### Question 3
> What packet number starts that app.php file?

From the pop up in question #2, there's a column labeled "Packet" that indicates `app.php` starts with packet `687`.

#### Question 4
> What is the IP of the Apache server?

Using the filter `http.server == "Apache"`, the search can be narrowed down to only Apache servers to find the source IP `192.185.57.242`.

#### Question 5
> What file is saved to the infected host?

It helps to narrow down the search by knowing three things: (1) the source was the Apache server, (2) the destination was the impacted machine, and (3) this interaction was over HTTP traffic by visiting a website. Using the filter `ip.src_host == "192.185.57.242" && ip.dst_host == "10.9.24.101" && http`, packet #687 caught my attention since it was the largest packet. It also stood out because it was found as part of question #2. Investigating the script, there's a base64-encoded string that gets written to disk with the file name `Ref_Sept24-2020.zip`.

#### Question 6
> Attackers used some bad TLS certificates in this traffic. Which countries were they registered to? Submit the names of the countries in alphabetical order separated by commas (Ex: Norway, South Korea).

To filter to only TLS traffic (and only traffic involving a certificates), I used the filter `(tls) && (tls.handshake.type == 11)`. From there, I added the column `CountryName` to make it easier to see the list without clicking into each packet individually. Unfortunately, we're only given the 2-alpha character abbreviations rather than the full names so I used [Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) to translate the results and get the answer `Ireland, Israel, South Sudan, United States`.

#### Question 7
> Is the host infected (Yes/No)?

Since the zip was successfully downloaded and the host began making network connections to suspicious IPs (based on the TLS certificates mentioned in question #6), the host machine should be considered infected.

## Objective #2: Windows Event Logs
> Investigate the Windows event log mystery in the terminal or offline. Get hints for this challenge by typing hint in the upper panel of the Windows Event Logs terminal

### Details

I used the native Event Viewer tool but this can also be solved via PowerShell.

Before starting investigating, I automatically filtered this to only include event ID 4104 since that captures the actual commands be executed.

#### Question 1
> What month/day/year did the attack take place? For example, 09/05/2021

Files of interest related to the recipe weren't modified until `12/24/2022`.

#### Question 2
> An attacker got a secret from a file. What was the original file's name?

Filtering the data to only the 24th, there was a command to get the contents of a `Recipe` file.

#### Question 3
> The contents of the previous file were retrieved, changed, and stored to a variable by the attacker. This was done multiple times. Submit the last full PowerShell line that performed on these actions.

Since the command line from question #2 included the cmdlet `Get-Content`, that keyword can be used to filter the data to find `$foo = Get-Content .\Recipe| % {$_ -replace 'honey', 'fish oil'}`

#### Question 4
> After storing the altered file contents into the varaible, the attacker used the variable to run a separate command that wrote the modified data to a file. This was done multiple timse. Submit the last full PowerShell line that performed only this action.

The varaible name `foo` is fairly unique to this dataset so we can filter on that keyword to find the PowerShell line `$foo | Add-Content -Path 'Recipe'`.

#### Question 5
> The attacker ran the previous command against a file multiple times. What is the name of this file?

Looking back at all the commands, we can see the targeted file was `Recipe.txt`

#### Question 6
> Were any files deleted? (Yes/No)

Yes, we can see the `del` command was run several times against `recipe_updated.txt`.

#### Question 7
> Was the original file (from question 2) deleted? (Yes/No)

No, the `del` command was never run against `Recipe`.

#### Question 8
> What is the event ID of the log that shows the actual command line used to delete the file?

For PowerShell Operational logs, event ID `4104` captures remote command lines.

#### Question 9
> Is the secret ingredient compromised? (Yes/No)

Yes, we can see from the command line in question #3, the keyword `honey` was replaced with `fish oil`.

#### Question 10
> What is the secret ingredient?

As mentioned in question #9, the secret ingredient is `Honey`

## Objective #3: Suricata Regatta
> Help detect this kind of malicious activity in the future by writing some Suricata rules. Work with Dusty Giftwrap in the Tolkien Ring to get some hints.

### Details

#### Prompt #1
> Use your investigative analysis skills and the suspicious.pcap file to help develop Suricata rules for the elves!
>
> There's a short list of rules started in suricata.rules in your home directory.
>
> First off, the STINC (Santa's Team of Intelligent Naughty Catchers) has a lead for us.  
> They have some Dridex indicators of compromise to check out.  
> First, please create a Suricata rule to catch DNS lookups for adv.epostoday.uk.  
> Whenever there's a match, the alert message (msg) should read `Known bad DNS lookup, possible Dridex infection.`  
> Add your rule to suricata.rules
> 
> Once you think you have it right, run ./rule_checker to see how you've done!  
> As you get rules correct, rule_checker will ask for more to be added.
> 
> If you want to start fresh, you can exit the terminal and start again or cp suricata.rules.backup suricata.rules
> 
> Good luck, and thanks for helping save the North Pole!

In this first prompt,  we're looking for DNS activity going externally, our filter should alert regardless of source or destination.

```
alert dns any any -> any any (msg:"Known bad DNS lookup, possible Dridex infection.";dns.query;content:"adv.epostoday.uk";)
```

#### Prompt #2:

> STINC thanks you for your work with that DNS record! In this PCAP, it points to 192.185.57.242.  
> Develop a Suricata rule that alerts whenever the infected IP address 192.185.57.242 communicates with internal systems over HTTP.  
> When there's a match, the message should read `Investigate suspicious connections, possible Dridex infection`

For this instance, we are looking at HTTP traffic between IP 192.185.57.242 and _any_ internal network address. One quirk I noticed is you had to specify `sid` to differentiate this from existing rules. Without `sid`, Suricata considered this a duplicate rule and threw an error.

```
alert http 192.185.57.242 any <> $HOME_NET any (msg:"Investigate suspicious connections, possible Dridex infection";sid:1001;)
```

#### Prompt #3:
> We heard that some naughty actors are using TLS certificates with a specific CN.   > Develop a Suricata rule to match and alert on an SSL certificate for heardbellith.Icanwepeh.nagcya.
> When your rule matches, the message (msg) should read `Investigate bad certificates, possible Dridex infection`

Here, we want TLS activity going both directions (internal and external) with a specific subject. Again, we need to specify SID otherwise Suricata throws errors and refuses to execute properly.

```
alert tls any any <> any any (msg:"Investigate bad certificates, possible Dridex infection";tls.subject:"CN=heardbellith.Icanwepeh.nagoya";sid:1002;)
```

#### Prompt #4:
> Let's watch for one line from the JavaScript: let byteCharacters = atob  
> Oh, and that string might be GZip compressed - I hope that's OK!  
> Just in case they try this again, please alert on that HTTP data with message `Suspicious JavaScript function, possible Dridex infection`

For this one, we need to search the HTTP response body between _any_ addresses for the JavaScrit keywords. 
```
alert http any any -> any any (msg:"Suspicious JavaScript function, possible Dridex infection";http.response_body;content:"let byteCharacters = atob";sid:1003;)
```

### References
- [Suricata Rule Format](https://suricata.readthedocs.io/en/suricata-6.0.0/rules/intro.html)
- [DNS](https://suricata.readthedocs.io/en/suricata-6.0.0/rules/dns-keywords.html)
- [HTTP](https://suricata.readthedocs.io/en/suricata-6.0.0/rules/http-keywords.html)
- [TLS/SSL](https://suricata.readthedocs.io/en/suricata-6.0.0/rules/tls-keywords.html)