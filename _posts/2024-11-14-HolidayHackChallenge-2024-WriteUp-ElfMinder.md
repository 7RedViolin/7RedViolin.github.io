---
layout: page
title: "Holiday Hack Challenge 2024 WriteUp - ElfMinder"
date: 2024-11-14 21:00:00 -0500
tags: ctf hhc-2024 web
intro: Assist Poinsettia McMittens with playing a game of Elf Minder 9000.
---

## Gold Objective
I've intentionally left the "Silver" objective out of this write up and, to quote my old math textbooks, will leave those as an exercise for the reader since no tricks or hacks are required to solve them. Instead, I'll focus on the much more interesting "Gold" objective that is available once you pass all previous levels.

> Congratulations! You've completed all levels!  
> That said, there is one level even our best Elf Minders have struggled to complete.  
> It's "A Real Pickle", to be sure.  
> We're not even sure it's solvable with our current tools.  
> I've added "A Real Pickle" to your level list on the main menu.  
> Can you give it a try?

We're then given the following layout and you'll notice there's no clear path to the finish flag since it's surrounded by boulders.

![](/images/holidayhackchallenge2024/elfminder_1.png)

I've heard rumors there's multiple ways to solve this and I'm still puzzling through the more "hacky" methods but in the meantime, here's the solution I used to complete the challenge.

First off, I noticed one the provided hints wasn't like the others and referenced the underlying Javascript:

> Elf Minder 9000: TODO  
> When developing a video game—even a simple one—it's surprisingly easy to overlook an edge case in the game logic, which can lead to unexpected behavior.

This sent me off on a quest to find comments (or TODO) items in the Javascript that suggest there may a bug or incomplete work. During that hunt, I found cool ascii art, an edit mode where you could build your own levels, and an awesome choice of variable name (`EMMEHGERDTICKSTHERESTICKSEVERYWHEREARHGHAHGREHUHGHH`). But ultimate, the piece of code I needed was in the `guide.js` file within the `getSpringTarget` function

![](/images/holidayhackchallenge2024/elfminder_2.png)

It took several debugging sessions to figure out this code tracked what direction you approached the spring and then would cycle through all possible points in that direction (either inline vertically or horizontally) to identify what path you could jump to. However, if the available path had an "entity" such as a tunnel or spring, it would default jump to `segment[0][0]`. 

From initial testing, `segment[0][0]` took you back to the beginning green flag. I tried altering the code itself to reference the specific coordinate of the finish flag at `[11, 8]` but would get an error each time which meant there had to be a way to control that line without changing the code.

I then reviewed how the `segment` array was built and discovered it depended on the order the segments were created and was _not_ sorted numerically. So I just needed to make sure the first path I created was at the finish flag so `segment[0][0]` would get me to the end.

Utlimately, my final set up looked like this:

![](/images/holidayhackchallenge2024/elfminder_3.png)