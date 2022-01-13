---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Greppin' for Gold"
date: 2022-01-12 21:00:00 -0600
tags: ctf kringlecon-2021
intro: Searching and aggregating logs in the command line
---

## Side Quest: Greppin' for Gold

![Goals](/images/kringlecon2021/grep_1.png)

With this puzzle, we have to grep the output of `nmap -oG`. The typcial format of these types of files is can be found on the official Nmap website:

![Nmap Greppable Output Format](/images/kringlecon2021/grep_2.png)

Question #1: What port does 34.76.1.22 have open?

Here it's just a basic grep command for the string `34.76.1.22`. I used the `-F` flag which searches for a fixed string and can make the search run slightly faster. The second line of the results clearly shows us port 62708 was open during the scan.

![Answer #1](/images/kringlecon2021/grep_3.png)

Question #2: What port does 34.77.207.226 have open?

This uses the same grep command as the first and gives us the answer 8080.

![Answer #2](/images/kringlecon2021/grep_4.png)

Question #3: How many hosts appear "Up" in the scan?

Now we're going to pipe the grep results through `wc -l` to get a line count - 26054.

![Answer #3](/images/kringlecon2021/grep_5.png)

Question #4: How many hosts have a web port open? (Let's just use ) TCP ports 80, 443, and 8080)

In this question, we're going to use `egrep` (we could have also used `grep -e`) to perform a regex search for all three ports. Then, the results will be piped to `wc -l` to get the final line count - 14372.

![Answer #4](/images/kringlecon2021/grep_6.png)

Question #5: How many hosts with status Up have no (detected) open TCP ports?

This solution is a lot more involved so we'll break it down step by step.

1. Use `cut -d " " -f2` to pull out the second column of a space-delimited table (i.e. save only the IP address from each line)

2. Use `grep -v "Nmap"` to collect all lines *except* those containing the string `Nmap`

3. Use `sort | uniq -c` to sort IPs in numerical order and then get a unique count of each.

4. Use `grep -F "1 "` to collect only the IPs that appear only once.

5. Use `wc -l` to get a line count.

We get 402 as the answer.

![Answer #5](/images/kringlecon2021/grep_7.png)

Question #6: What's the greatest number of TCP ports any one host has open?

Again, we'll break this down step by step since this has several commands.

1. Use `grep -F "Ports"` to collect the lines that contain the keyword `Ports`

2. Use `awk -F "open" '{print NF-1}'` to count each instance of the word `open` in a given line

3. Use `sort | uniq` to find unique aggregates

We're looking for the greatest number which is 12.
![Answer #6](/images/kringlecon2021/grep_8.png)

Hindsight being 20/20, I could have piped the output through `sort -n -r | head -1` which would have sorted the numbers in descending order and then returned the top result.

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
* [Nmap Greppable Format](https://nmap.org/book/output-formats-grepable-output.html)