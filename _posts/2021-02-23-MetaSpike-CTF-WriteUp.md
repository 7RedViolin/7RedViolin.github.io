---
layout: page
title: "MetaSpike CTF - (Un)authorized Access & The REST is History"
date: 2021-02-23 21:00:00 -0600
tags: email ctf api
intro: Over the last couple months, MetaSpike hosted an email forensics CTF. I wasn't able to get in on it until the very end but I enjoyed the puzzles they presented. It's rare to find CTFs dedicated to a specific area of forensics so I was excited to try out the challenges.
---
Over the last couple months, MetaSpike hosted an email forensics CTF. I wasn't able to get in on it until the very end but I enjoyed the puzzles they presented. It's rare to find CTFs dedicated to a specific area of forensics so I was excited to try out the challenges.

The ones I focused on were related to Google APIs. However, if you're curious about the earlier puzzles, Phill Moore has excellent write ups that can be found on his [ThinkDFIR blog](https://thinkdfir.com/).

## (Un)authorized Accessed

>During a recent search & seizure, you were able to extract the following information from a suspect's devices:  
>Client ID: 182818710541-mn63dksdjh44sho1fs3jaiinljoj1lnh.apps.googleusercontent.com  
> Client Secret: GBhMGNPcZiqXLfOMxT7v7Ur0  
> Refresh Token: 1//04SVLXWq0TK7HCgYIARAAGAQSNwF-L9IrFaEKgxVUl3Ismo9dmDJpjZrI0Uu4-n3Yjm1zCLO_pQZdvjgxA9dbp8yjQ6SrQ-F3mto  
> Email: ornatdilwen@gmail.com
> Scope: https://www.googleapis.com/auth/gmail.readonly  
> Leveraging Google's OAuth 2.0 Playground, authenticate with the suspect's mailbox and list the forwarding addresses for their account. Enter the forwarding email address that has a verification status of "pending".

I start by using the refresh token to get a new access token using the settings outlined below in Postman.

![](/images/metaspikectf/postman_unauth_1.png)

I then was able to use that access token to query the user's inbox. It took some time reading up on the documentation but I found an API dedicated to listing forwarding address.

![](/images/metaspikectf/postman_unauth_2.png)

This resulted in the flag: `flag{76a4ca21c2d3@proksimiti.com}`

## The REST is History (Part 1)

> Your work on the last challenge, (Un)authorized Access, paved the way to a detailed investigation of the suspect's online activity.  
> One data point that is of interest now is a message in the suspect's Gmail mailbox. The message was believed to have been labeled with the "PFAS" label at some point in time.  
> Find the message and enter its Message-Id*. You can use the same authentication technique as you did during (Un)authorized Access. Refer to the updated authentication details in the archived copy of (Un)authorized Access.  
> *: The unique identifier found in the "Message-Id" header field. Not the "id" field used in Gmail API to address messages.

Using the access token from the previous challenge, I was able to list all available labels for the target mailbox.

![](/images/metaspikectf/postman_rest1_1.png)

Here, we can see the target label `PFAS` has the label ID of `Label_1219094403288520213` which we can use to filter the messages:

![](/images/metaspikectf/postman_rest1_2.png)

Unfortunately, there weren't any messages with the label currently. This made me review the wording of the challenge and I noticed the phrase `have been labeled` - could this indicate the target message had the `PFAS` label removed at some point?

If my hunch was correct, I could use the Google's history API to see when a label was added or removed.

![](/images/metaspikectf/postman_rest1_3.png)

This search brought back exactly one message. I could then use the messageId to pull out that specific email and get the flag.

![](/images/metaspikectf/postman_rest1_4.png)

The gave us the answer `flag{20210216043536.602b4b98c7ebdf3b47fc6627@sailthru.com}`

## The REST is History (Part 2)

> Congratulations on locating that crucial message! You are now asked to determine the earliest time the "PFAS" label could have been removed from the message based on the information available to you.  
> Enter the timestamp in UTC in the following format: yyyy-mm-dd hh:mm:ss (e.g., 2005-11-20 13:17:51)

Now I'm looking for when the label was removed . . . Reading the documentation on the Google history list API, the entries are created in chronological order. My train of thought was if I could find a message that was delivered right before the label was removed, that should give me a good approximation.

From the screenshot above, it looked like the history ID of the label being removed was 5415. So I was looking for a message that was received with a history ID less than 5415.

![](/images/metaspikectf/postman_rest2_1.png)

The closest I could find was history ID 5271. This gave me a pivot point into the specific email:

![](/images/metaspikectf/postman_rest2_2.png)

Doing a bit of datetime math, this made the answer to be `flag{2021-02-16 04:54:59}`.

## References
* [Refreshing an Access Token](https://www.oauth.com/oauth2-servers/making-authenticated-requests/refreshing-an-access-token/)
* [Google API Documentation](https://developers.google.com/gmail/api/reference/rest)
