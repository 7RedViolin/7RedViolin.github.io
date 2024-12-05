---
layout: page
title: "Holiday Hack Challenge 2024 WriteUp - Drone Path"
date: 2024-12-03 21:00:00 -0500
tags: ctf hhc-2024 kml
intro: Help the elf defecting from Team Wombley get invaluable, top secret intel to Team Alabaster.
---

## Silver Objective

For this puzzle, we're given the challenge of finding a way to login to the drone program. However, we're only given a KML file with the hint that it contains the credentials.

![](/images/holidayhackchallenge2024/drone_path_1.png)

I had to read up on KML files but it basically contains coordinates of the drone's flight path. With that in mind, I was curious to see this plotted out and learned Google Earth provides that very capability! Uploading the KML, there was very clearly a path over Antarctica that appeared to be a password.

![](/images/holidayhackchallenge2024/drone_path_3.png)

From there, I assumed the file name `fritjolf-Path` contained the user account and plugged that into the login page. 

From there, I now had access to several different pages including an admin login screen, a drone search tab, and a user profile page

![](/images/holidayhackchallenge2024/drone_path_11.png)

On the user profile, I found a CSV for download that contained a sort of drone system log with information like altitude, longitude, latitude, and battery information. Of course, my mind focused on the latitude and longitude because I assumed this step would follow the same process as the previous except that I would have to build a KML file myself.

![](/images/holidayhackchallenge2024/drone_path_2.png)

Unfortunately, plugging that new data into Google Earth didn't provide such as easy answer but rather a seemingly random shape.

![](/images/holidayhackchallenge2024/drone_path_4.png)

I tried several things like identifying cities nearby the points or thinking the shape was a rough arrow and pointing northwest at something specific. It wasn't until I started zooming in very closely to each point that I noticed the aerial view of the landmarks formed the letters: `E L F - H A W K`.

I first assumed this was the password for the admin console but soon learned it was the name of an actual drone.

![](/images/holidayhackchallenge2024/drone_path_5.png)

And yet _another_ CSV file to download but this time, it had over 3,000 entries. I approached this CSV like I did the last one and made a KML file for use in Google Earth but only got random lines criss-crossing the globe.

I got a nice hint from the Holiday Hack Discord channel to try and view the longitude/latitude on a flat plane rather than a globe. So I threw the CSV into a Google Sheet and created a line chart.

![](/images/holidayhackchallenge2024/drone_path_6.png)

Now that I had what was clearly a password, I entered it into the admin console and solved the Silver Objective!

![](/images/holidayhackchallenge2024/drone_path_7.png)

## Gold Objective

For the Gold level, the elf gave the following hint

> But I need you to dig deeper. Make sure you’re checking those file structures carefully, and remember—rumor has it there is some injection flaw that might just give you the upper hand. Keep your eyes sharp!

The first injection flaw that came to mind was SQL injection simply because it is the one I'm most familiar with and is pretty straightforward in testing. Since there were only two pages that accepted input, it was trivial to discover the drone search page was vulnerable.

![](/images/holidayhackchallenge2024/drone_path_8.png)

When exploiting the vulnerability, it only gave me the drone names and not all the comments so I went down the list to see what more information I could find. The drone of interest turned out to be `Pigeon-Lookalike-v4` since it had an interesting note on TRUE and FALSE carving.

![](/images/holidayhackchallenge2024/drone_path_9.png)

Going back to the last CSV I got with the thousands of lines, I noticed there were several columns that only had true and false values. I first attempted to filter to lines with _only_ `true` values but that proved impossible. Next, I noticed some lines had only `false` values and thought I should carve those out and plot the longitude and latitudelines with at least one `true` entry. Neither approach gave me anything.

Then, I had a thought to turn the values to 1's and 0's to make a binary string and convert using CyberChef. This gave me some cool drone ASCII art and the final password

![](/images/holidayhackchallenge2024/drone_path_12.png)

I plugged that into the admin console and achieved the Gold Objective!

![](/images/holidayhackchallenge2024/drone_path_10.png)