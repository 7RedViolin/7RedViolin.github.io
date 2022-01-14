---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Splunk"
date: 2022-01-13 21:00:00 -0500
tags: ctf kringlecon-2021 splunk
intro: Dashing through the logs
---

## Objective: Splunk!
> Help Angel Candysalt solve the Splunk challenge in Santa's great hall. Fitzy Shortstack is in Santa's lobby, and he knows a few things about Splunk. What does Santa call you when when you complete the analysis?

**Question #1**: Capture the commands Eddie ran most often, starting with git. Looking only at his process launches as reported by Sysmon, record the most common git-related CommandLine that Eddie seemed to use.

We needed to filter the logs to only include Sysmon event IDs 1 (process creation) where the command line must include `git`. We then had to aggregate the results based on the command line. The top line would be our answer.

Query: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 CommandLine=*git*| stats count by CommandLine`

![Answer #1](/images/kringlecon2021/splunk_1.png)

**Question #2**: Looking through the git commands Eddie ran, determine the remote repository that he configured as the origin for the 'partnerapi' repo. The correct one!

I had to look up git commands but the remote repo can be set when calling `origin`. In this query, instead of creating an aggregate, we want to generate a table of results sorted by time so we get the most recent settings. In this case, `git@github.com:elfnp3/partnerapi.git`

Query: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 "origin" | table UtcTime, CommandLine`

![Answer #2](/images/kringlecon2021/splunk_2.png)

**Question #3**: Eddie was running Docker on his workstation. Gather the full command line that Eddie used to bring up a the partnerapi project on his workstation.

Not being super familiar with running Docker, all I really knew to filter by was the keyword `docker` but that worked out in my favor since the answer was `docker compose up`.

Query: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 "docker" | table  UtcTime, CommandLine`

![Answer #3](/images/kringlecon2021/splunk_3.png)

**Question #4**: Eddie had been testing automated static application security testing (SAST) in GitHub. Vulnerability reports have been coming into Splunk in JSON format via GitHub webhooks. Search all the events in the main index in Splunk and use the sourcetype field to locate these reports. Determine the URL of the vulnerable GitHub repository that the elves cloned for testing and document it here. You will need to search outside of Splunk (try GitHub) for the original name of the repository.

For this query, we are looking at GitHub logs rather than Sysmon data. We also searching for columns related to repo URLs. I aggregated the `repository.url` to get a sense of which were most common to help prioritize the search outside of Splunk.

Query: `index=main sourcetype=github_json | stats count by repository.url`

![Answer #4 - part 1](/images/kringlecon2021/splunk_4.png)

![Answer #4 - part 2](/images/kringlecon2021/splunk_5.png)

**Question #5**: Santa asked Eddie to add a JavaScript library from NPM to the 'partnerapi' project. Determine the name of the library and record it here for our workshop documentation.

Here again I'm not super familiar with the program or method but I have a keyword (in this case `npm`) I can use to filter and find the library `holiday-utils-js`. 

Query: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 CommandLine=*node*npm* | table UtcTime, CommandLine`

![Answer #5](/images/kringlecon2021/splunk_6.png)

**Question #6**: Another elf started gathering a baseline of the network activity that Eddie generated. Start with their search and capture the full process_name field of anything that looks suspicious.

In this case, the initial query `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=3 user=eddie NOT dest_ip IN (127.0.0.*) NOT dest_port IN (22,53,80,443) | stats count by dest_ip dest_port` gave the results:

![Starting point](/images/kringlecon2021/splunk_7.png)

Using that info, I expanded on the original query to focus on the two destination IPs and return only process names to get the answer `usr/bin/nc.openbsd`.

Query: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=3 user=eddie NOT dest_ip IN (127.0.0.*) NOT dest_port IN (22,53,80,443)   (dest_ip="54.175.69.219" OR dest_ip="192.30.255.113") | table process_name`

![Answer #6](/images/kringlecon2021/splunk_8.png)

**Question #7**: Uh oh. This documentation exercise just turned into an investigation. Starting with the process identified in the previous task, look for additional suspicious commands launched by the same parent process. One thing to know about these Sysmon events is that Network connection events don't indicate the parent process ID, but Process creation events do! Determine the number of files that were accessed by a related process and record it here.

To keep the momentum from the previous question, I filtered the last query used by process_name and had it return all the possible PID values. I'm still not entirely sure what the difference is between the three.

Query #1: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=3 user=eddie NOT dest_ip IN (127.0.0.*) NOT dest_port IN (22,53,80,443)   (dest_ip="54.175.69.219" OR dest_ip="192.30.255.113") AND process_name="/usr/bin/nc.openbsd" | table ProcessID, ProcessId, PID`

![Results for query #1](/images/kringlecon2021/splunk_9.png)

From there, I filtered the Sysmon process creation events (ID 1) by PID to get the parent process.

Query #2: `Using PID, let's search the process stuff
index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 AND PID=6791 | table parent_process_id`

![Results for query #2](/images/kringlecon2021/splunk_10.png)

Now searching based on parent pid, I saw there were 6 files accessed.

Query #3: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 AND parent_process_id=6788 | table UtcTime, CommandLine`

![Results for query #3](/images/kringlecon2021/splunk_11.png)

**Question #8**: Use Splunk and Sysmon Process creation data to identify the name of the Bash script that accessed sensitive files and (likely) transmitted them to a remote IP address.

Here I just wanted to see all parent fields of PID 6788 to learn the suspicious Bash script was `preinstall.sh`.

Query: `index=main sourcetype=journald source=Journald:Microsoft-Windows-Sysmon/Operational EventCode=1 AND PID=6788 | table parent*`

![Answer #8](/images/kringlecon2021/splunk_12.png)

After answering question #8, a banner popped up at the top of the page with the flag!

![Final banner](/images/kringlecon2021/splunk_13.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [Splunk Cheat Sheet](https://www.splunk.com/pdfs/solution-guides/splunk-quick-reference-guide.pdf)