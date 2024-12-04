---
layout: page
title: "Holiday Hack Challenge 2024 WriteUp - KQL"
date: 2024-12-03 21:00:00 -0500
tags: ctf hhc-2024 kql
intro: Use KQL to investigate recent cyber attacks at the North Pole.
---

## Background Information
> This is weird, I got some intel about an imminent attack.
> 
> Pepper Minstix here! I’ve got urgent news from neutral ground.
> 
> The North Pole is facing a serious cyber threat, and it’s putting all the factions on edge. The culprits? Some troublemakers from Team Wombley.
> 
> They’ve launched a barrage of phishing attacks, ransomware, and even some sneaky espionage, causing quite the stir.
> 
> It’s time to jump into action and get cracking on this investigation—there’s plenty of cyber-sleuthing to do.
> 
> You’ll be digging into KQL logs, tracking down phishing schemes, and tracing compromised accounts like a seasoned pro.
> 
> Malware infections have already breached Alabaster Snowball’s systems, so we need swift action.
> 
> Your top mission: neutralize these threats, with a focus on the ransomware wreaking havoc from Team Wombley.
> 
> It’s a hefty challenge, but I know you’re up to it. We need your expertise to restore order and keep the peace.
> 
> You’ve got the tools, the skills, and the know-how—let’s show Team Wombley we mean business.
> 
> Ready to dive in? Let's defend the North Pole and bring back the holiday harmony!

Another personal goal I set for myself was to avoid hardcoding any values in the queries, attempt to answer the question using a single query, and getting a query output that doesn't require any additional parsing or analysis to find the answer.

With that in mind, let's dive in!

## KQL 101
This challenge started off slow with some introductory questions about KQL where the query was already provided so people could get used to the console. I've skipped those questions and plan to dive right into the interesting ones below!

> Can you find out the name of the Chief Toy Maker?

For this question, we're given the specific value we should search so we can use the `==` operator for an exact match.

```
Employees
| where role == "Chief Toy Maker"
| project name
```

> How many emails did Angel Candysalt receive?

This will need to be a two-part solution since we aren't given Angel's email address and the `Email` table doesn't include the name. We'll also need to use a sort of aggregate operator to get a count.

First off, I'll query the `Employees` table to get the email and then join that with the `Email` table to get an number of how many messages.

```
Employees
| where name == 'Angel Candysalt'
| project email_addr
| join kind=inner Email on $left.email_addr == $right.recipient
| count
```

> How many distinct recipients were seen in the email logs from twinkle_frostington@santaworkshopgeeseislands.org?

This question requires a different aggregate operator than the last one since we're looking for a distinct count and no duplicates.

```
Email
| where sender == 'twinkle_frostington@santaworkshopgeeseislands.org'
| summarize dcount(recipient)
```

> How many distinct websites did Twinkle Frostington visit?

And now to put the last two questions together, we're going to correlate the user to their assigned IP address and then use that source IP to identify how many unqiue URLs were visited.

```
Employees
| where name == "Twinkle Frostington"
| project ip_addr
| join kind=inner OutboundNetworkEvents on $left.ip_addr == $right.src_ip
| summarize dcount(url)
```

> How many distinct domains in the PassiveDns records contain the word green?

Since we're looking for any domain with the word `green`, we'll use the `contains` operator for a substring search.

```
PassiveDns
| where domain contains "green"
| summarize dcount(domain)
```

> How many distinct URLs did elves with the first name Twinkle visit?

Very similar to the last few queries, but this time I'm using the `startswith` operator to ensure we only have elves with the first name exactly `Twinkle` (hence the extra space at the end).

```
Employees
| where name startswith "Twinkle "
| distinct ip_addr
| join kind=inner OutboundNetworkEvents on $left.ip_addr == $right.src_ip
| summarize dcount(url)
```

## Operation Surrender

> Team Alabaster, with their limited resources, was growing desperate for an edge over Team Wombley. Knowing that a direct attack would be costly and difficult, they turned to espionage. Their plan? A carefully crafted phishing email that appeared harmless but was designed to deceive Team Wombley into downloading a malicious file. The email contained a deceptive message with the keyword “surrender” urging Wombley’s members to click on a link.  
> Who was the sender of the phishing email that set this plan into motion?

Here's a new aggregation operator called `distinct` we can use since we assume there will be multiple emails but all with the same sender.

```
Email
| where subject contains "surrender"
| distinct sender
```

> How many elves from Team Wombley received the phishing email?

This answer uses the familiar aggregation operator `dcount()` to get the number of unique recipients.

```
Email
| where subject contains "surrender"
| summarize dcount(recipient)
```

> What was the filename of the document that Team Alabaster distributed in their phishing email?

The query I used here isn't nearly as elegant as the previous ones and rquires some additional analysis. It will return all the unique links found in the phishing emails but the analyst will need to review the links to determine the actual file name.

```
Email
| where subject contains "surrender"
| distinct link
```

> Who was the first person from Team Wombley to click the URL in the phishing email?

This is so far the most complex query. It can be broken down into three simple parts, though. 

We first start with identifying the unique links found in the `Email` table. Then, we correlate those links to the `OutboundNetworkEvents` table to identify the source IP responsible for visiting the site. From there, we can use the IP address to identify the associated user via the `Employees` table. 

To get the first user that clicked, we can sort the results based on the timestamp of the network event and only return the top hit.

```
Email
| where subject contains "surrender"
| distinct link
| join kind=inner OutboundNetworkEvents on $left.link == $right.url
| join kind=inner Employees on $left.src_ip == $right.ip_addr
| order by timestamp asc
| limit 1
| project name
```

> What was the filename that was created after the .doc was downloaded and executed?

Another complex query that builds upon the previous answer. 

Here, we're taking our last query and joining it to the `FileCreationEvents` table based on the associated hostname to see all the files recently written to disk. However, we're most interested in files that were created after the email was delivered (hence the `timestamp1 > timestamp` filter) but only if the file was created shortly afterwards within an hour (so we include the operator `datetime_diff`).

```
Email
| where subject contains "surrender"
| distinct link
| join kind=inner OutboundNetworkEvents on $left.link == $right.url
| join kind=inner Employees on $left.src_ip == $right.ip_addr
| order by timestamp asc
| limit 1
| project timestamp, hostname
| join kind=inner FileCreationEvents on $left.hostname == $right.hostname
| where timestamp1 > timestamp and datetime_diff('hour', timestamp1, timestamp) < 1
| distinct filename
```

## Operation Snowfall

> What was the IP address associated with the password spray?

With the behavior of a password spray, I'd expect to see a bunch of failed logins. So this query searches specifically for failed login attempts, aggregates the results by source IP, and gets the entry with the highest entry count.

```
AuthenticationEvents
| where result == "Failed Login"
| summarize count() by src_ip
| sort by count_ desc
| limit 1
```

> How many unique accounts were impacted where there was a successful login from 59.171.58.12?

We can use the previous query that got us the offending IP and correlate that the successful logins to identify a unique list of usernames.

```
AuthenticationEvents
| where result == "Failed Login"
| summarize count() by src_ip
| sort by count_ desc
| limit 1
| join kind=inner (AuthenticationEvents | where result == "Successful Login") on $left.src_ip == $right.src_ip
| summarize dcount(username)
```

> What service was used to access these accounts/devices?

I'll admit I struggled to find the answer here. I expected to find information in the network telemetry to tell me what port was involved but I was overcomplicating the problem. The solution was found in the `description` field of the `AuthenticationEvents` table.

```
AuthenticationEvents
| where result == "Failed Login"
| summarize FailedAttempts = count() by src_ip
| sort by FailedAttempts desc
| limit 1
| join kind=inner (AuthenticationEvents | where result == "Successful Login") on $left.src_ip == $right.src_ip
| distinct description
```

> What file was exfiltrated from Alabaster’s laptop?

This solution filters the previous query to only Alabaster's username and joins it to the `ProcessEvents` table by hostname to get the processes recently executed. It takes some analysis work but while several files were deleted or copied based on the process commandlines, there is only one file that was actually moved. 

```
AuthenticationEvents
| where result == "Failed Login"
| summarize FailedAttempts = count() by src_ip
| sort by FailedAttempts desc
| limit 1
| join kind=inner (AuthenticationEvents | where result == "Successful Login") on $left.src_ip == $right.src_ip
| where username startswith "alsnowball"
| join kind=inner ProcessEvents on $left.hostname == $right.hostname
| where timestamp1 > timestamp
| project timestamp1, process_commandline
| order by timestamp1 asc
```

> What is the name of the malicious file that was run on Alabaster's laptop?

To answer this question, I used the same query as previously and identified the malicious file based on the name.

## Echoes in the Frost

> What was the timestamp of first phishing email about the breached credentials received by Noel Boetie?

This is a two-part query where I first identified Noel's email address in the `Employees` table and then correlated it to entries in the `Email` table filtered only to messages that had a subject containing the keyword `breach`. From there, I sorted by timestamp so I could return the earliest entry.

```
Employees
| where name == "Noel Boetie"
| project email_addr
| join kind=inner Email on $left.email_addr == $right.recipient
| where subject contains "breach"
| project timestamp
| order by timestamp asc
| limit 1
```

> When did Noel Boetie click the link to the first file?

Building on the previous query, I added a join to the `OutboundNetworkEvents` based on the link in the email to identify the timestamp of the network connection.

```
Employees
| where name == "Noel Boetie"
| project email_addr
| join kind=inner Email on $left.email_addr == $right.recipient
| where subject contains "breach"
| project timestamp, link
| order by timestamp asc
| limit 1
| join kind=inner OutboundNetworkEvents on $left.link == $right.url
| project timestamp1
```

> What was the IP for the domain where the file was hosted?

This solution also builds off the first query in this section first by parsing the URL using the `parse_url()` funtion that can pull out the domain (also referred to as `Host`) which can then be correlated to the `PassiveDns` table to get the associated destination IP.

```
Employees
| where name == "Noel Boetie"
| project email_addr
| join kind=inner Email on $left.email_addr == $right.recipient
| where subject contains "breach"
| extend domain = tostring(parse_url(link)["Host"])
| distinct domain
| join kind=inner PassiveDns on $left.domain == $right.domain
| distinct ip
```

> Let’s take a closer look at the authentication events. I wonder if any connection events from 182.56.23.122. If so what hostname was accessed?

Using the query from above, I joined the `AuthenticationEvents` table based on IP to get the targeted hostname involved in the login attempt.

```
Employees
| where name == "Noel Boetie"
| project email_addr
| join kind=inner Email on $left.email_addr == $right.recipient
| where subject contains "breach"
| extend domain = tostring(parse_url(link)["Host"])
| distinct domain
| join kind=inner PassiveDns on $left.domain == $right.domain
| distinct ip
| join kind=inner AuthenticationEvents on $left.ip == $right.src_ip
| project hostname
```

> What was the script that was run to obtain credentials?

After the targeted hostname was identified, I joined the results to the `ProcessEvents` table to get a list of process command lines. The results were short so it didn't take long to review the output and identify the credential theft tool.

```
Employees
| where name == "Noel Boetie"
| project email_addr
| join kind=inner Email on $left.email_addr == $right.recipient
| where subject contains "breach"
| extend domain = tostring(parse_url(link)["Host"])
| distinct domain
| join kind=inner PassiveDns on domain
| distinct ip
| join kind=inner AuthenticationEvents on $left.ip == $right.src_ip
| project hostname
| join kind=inner ProcessEvents on hostname
| project process_commandline
```

> What is the timestamp where Noel executed the file?

This was the first question I came across where I couldn't create an elegant single query to answer the question. Instead, I had to break it up into two parts: one query to find the file name and a second query to identify the execution time.

```
Employees
| where name == "Noel Boetie"
| project email_addr, hostname
| join kind=inner Email on $left.email_addr == $right.recipient
| where subject contains "breach"
| project timestamp, hostname, link
| order by timestamp asc
| limit 1

ProcessEvents
| where hostname == "Elf-Lap-A-Boetie" and process_commandline contains "echo.exe"
| project timestamp
```

> What domain was the holidaycandy.hta file downloaded from?

This query assumes the file name is included in the URL path.

```
OutboundNetworkEvents
| where url contains "holidaycandy.hta"
| extend domain = tostring(parse_url(url)["Host"])
| distinct domain
```

> An interesting series of events has occurred: the attacker downloaded a copy of frosty.txt, decoded it into a zip file, and used tar to extract the contents of frosty.zip into the Tasks directory.  
> What was the first file that was created after extraction?

For this solution, I started with ProcessEvents involving commandlines referencing the `frosty.zip` file but parsed down to the earliest timestamp (hence the `| summarize min(timestamp) by hostname` clause). I then joined the results to the `FileCreationEvents` table by hostname to see what files were created shortly after that minimum timestamp.

```
ProcessEvents
| where process_commandline contains "frosty.zip"
| summarize min(timestamp) by hostname
| join kind=inner FileCreationEvents on hostname
| where timestamp > min_timestamp
| order by timestamp asc
| limit 1
| project filename
```

> What is the name of the property assigned to the new registry key?

Since we didn't have a table dedicated to registry modifications, I assumed this took place in a command line and used the traditional prefixes `HLKM` (for `hkey_local_machine`), `HKCU` (for `hkey_current_user`).

```
ProcessEvents
| where process_commandline contains "HKLM" or process_commandline  contains "HKCU"
| project process_commandline
```

## KQL Command References
- [dcount()](https://learn.microsoft.com/en-us/kusto/query/dcount-aggregation-function?view=microsoft-fabric)
- [contains](https://learn.microsoft.com/en-us/kusto/query/contains-operator?view=microsoft-fabric)
- [startswith](https://learn.microsoft.com/en-us/kusto/query/startswith-operator?view=microsoft-fabric)
- [distinct](https://learn.microsoft.com/en-us/kusto/query/distinct-operator?view=microsoft-fabric)
- [datetime_diff()](https://learn.microsoft.com/en-us/kusto/query/datetime-diff-function?view=microsoft-fabric)
- [parse_url()](https://learn.microsoft.com/en-us/kusto/query/parse-url-function?view=microsoft-fabric)
- [min()](https://learn.microsoft.com/en-us/kusto/query/min-aggregation-function?view=microsoft-fabric)