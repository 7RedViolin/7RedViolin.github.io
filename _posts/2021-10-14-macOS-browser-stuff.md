---
layout: page
title: "macOS Browser Stuff"
date: 2021-10-13 13:00:00 -0000
tags: macOS forensics browsers
intro: Browser artifacts and EDR data you should expect when investigating macOS devices.
---
From a forensic perspective, browser artifacts are practically the same across operating systems - the only difference is the location of the artifacts. In EDR data, the process names for Windows and macOS are different.

The artifacts I've called out are far from comprehensive but are what I consider the most useful. SANS has provided a thorough list for Google Chrome and Firefox via their "Evidence Of" poster. You can also see the available browser artifacts by simply reviewing the contents of their home directory.

## Safari
- Location `~/Library/Safari`
- Artifacts of Interest
    - `History.db` SQLite formatted database. However, in older versions of Safari, it will be in plist format. By default, Safari history is only stored for one year.
    - `TopSites.plist` By default, this is the top 12 sites visited.
    - `Downloads.plist` By default, the retention is set to the last 20 downloads for one day. Once Safari is opened on the next day, the file is cleared.
- EDR process name `Safari` and `com.apple.WebKit.Networking`
    - Safari is built on top of the WebKit open-source browser so you will most commonly see network connections and filemods originating from the `com.apple.WebKit.Networking` process. As a side note, several other Apple applications are built on WebKit.

## Google Chrome
- Location `~/Library/Application Support/Google/Chrome/Default`
- Artifacts
    - `History` A SQLite database containing URLs, timestamps, visit counts, etc.
- EDR process name `Google Chrome` and `Google Chrome Helper`
    - On macOS, the process `Google Chrome Helper` will contain data related to ad traffic and any other similar connections to remote servers. All other netconns and filemods should be tied to the `Google Chrome` process name. 
## Mozilla Firefox
- Location `~/Library/Application/Support/Mozilla/Firefox/****.default/` with `***` being a randomized alphanumeric string of varying length
- Artifacts
    - `places.sqlite` SQLite database containing browser history.
- EDR process name `Firefox`
    - I haven't seen any other process name related to Mozilla but all activity appears to be tied to the `Firefox` process.

## References
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Open source tool not just for browsers but any SQLite databases.
- [BrowsingHistoryView](https://www.nirsoft.net/utils/browsing_history_view.html) - A free GUI tool that can take a variety of inputs (specific user folder, specific history file) and create a normalized table of events. 
- [SANS EvidenceOf Poster](https://www.sans.org/posters/windows-forensic-analysis/) - Free poster that outlines not only browser forensics but also other Windows artifacts. As mentioned above, I haven't noticed browser artifacts don't change very much between OS systems so even though the poster says "Windows Forensic Analysis", the browser section is still applicable to macOS. This link requires you to set up a free account to download directly from SANS but a quick Google search can surface screenshots without requiring further setup.