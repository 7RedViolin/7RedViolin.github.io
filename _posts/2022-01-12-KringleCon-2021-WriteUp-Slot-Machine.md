---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Slot Machine Investigation"
date: 2022-01-12 22:00:00 -0500
tags: ctf kringlecon-2021 web
intro: Can we beat the odds at a slot machine?
---

## Objective: Slot Machine Investigation

> Test the security of Jack Frost's slot machines. What does the Jack Frost Tower casino security team threaten to do when your coin total exceeds 1000? Submit the string in the server data.response element.

In this challenge, we're given a link to Jack Frost's slot machine and told to collect more than 1000 coins. We start out with 100 coins but just casually playing the slots makes it clear this machine favors the house.

![Slot machine](/images/kringlecon2021/slot_machine_1.png)

It's obvious we're expected to "hack" the game so I opened up the dev tools of the browser to see the requests and responses. 

![Headers](/images/kringlecon2021/slot_machine_2.png)

![Request parameters](/images/kringlecon2021/slot_machine_3.png)

There wasn't anything in the headers to adjust but the request parameters appeared to change with each spin. It took me a while to figure out Chrome doesn't allow you to edit and resend requests - but Firefox has that feature built-in. Once I switched to Firefox, I was able to play around with the `betamount`, `numline`, and `cpl`.

Any changes to `betamount` had to correspond to what was already known - I couldn't bet 300 coins if I only had 200 coins. Otherwise, I would get an error response.

The parameter `numline` would error out if I chose random numbers and it didn't appear to make a difference to the winning amount.

However, the `cpl` parameter seemed to be less finicky. After a couple tests, I learned negative numbers were accepted by the parameter and gave me extra coins!

![Request](/images/kringlecon2021/slot_machine_4.png)

Here we can see my coin count is now above 1000!

![Response](/images/kringlecon2021/slot_machine_5.png)

And in the response, there's the secret message we've been looking for:

![Message](/images/kringlecon2021/slot_machine_6.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [Edit & Resend Requests](https://itectec.com/superuser/how-to-edit-parameters-sent-through-a-form-on-the-firebug-console/)