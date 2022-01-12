---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - ExifTool"
date: 2022-01-11 21:00:00 -0500
tags: ctf kringlecon-2021 forensics
intro: How to quickly search metadata of multiple files
---

The holidays aren't complete without taking part in the Holiday Hack Challenge (also known as KringleCon) hosted by SANS. With challenges ranging from network and endpoint forensics, threat hunting, pen testing, and everything in between, there's always something to learn. 

The puzzles are set up in story form where there are main objectives that unlock parts of the narrative with mini side quests that, if solved, can provide hints to the larger puzzles. In this series of posts, I'll be adding write ups of some of the more interesting/unique objectives and side quests.

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## Side Quest: ExifTool Metadata

> Help! That wily Jack Frost modified one of our naughty/nice records, and right before Christmas! Can you help us figure out which one? We've installed exiftool for your convenience!

We're given a bunch of DOCX files and need to find which was changed by Jack Frost. While we could investigate the files one by one, `exiftool` allows us to analyze multiple files at a time and pull out only the relevant fields. I added the step to grep for the keyword "Jack Frost" and also add the option -B1 to make sure the file name (which appears one line before the modifying user) is included in the output.

![ExifTool Solution](/images/kringlecon2021/exiftool_solution.png)

### References
* [ExifTool options and examples](https://exiftool.org/examples.html)
* [Grep options](https://ss64.com/bash/grep.html)
